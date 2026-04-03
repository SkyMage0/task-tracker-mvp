# web_app.py - Веб-версия трекера задач
from flask import Flask, render_template, request, redirect, url_for, jsonify
import tasks

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница - список задач"""
    all_tasks = tasks.load_tasks()
    all_tasks = tasks.migrate_old_tasks(all_tasks)
    
    # Сортируем: сначала невыполненные, потом по приоритету
    priority_order = {"high": 0, "medium": 1, "low": 2}
    all_tasks.sort(key=lambda x: (x['completed'], priority_order.get(x['priority'], 2)))
    
    # Подсчет статистики
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t['completed'])
    pending = total - completed
    
    stats = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'progress': round(completed/total*100, 1) if total > 0 else 0
    }
    
    return render_template('index.html', tasks=all_tasks, stats=stats)

@app.route('/add', methods=['POST'])
def add_task_web():
    """Добавляет новую задачу из веб-формы"""
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')
    deadline = request.form.get('deadline', '')
    
    if description:
        tasks_list = tasks.load_tasks()
        new_task = {
            'id': len(tasks_list) + 1,
            'description': description,
            'completed': False,
            'priority': priority,
            'created_at': __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M"),
            'deadline': deadline if deadline else None
        }
        tasks_list.append(new_task)
        tasks.save_tasks(tasks_list)
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task_web(task_id):
    """Отмечает задачу выполненной"""
    tasks_list = tasks.load_tasks()
    for task in tasks_list:
        if task['id'] == task_id:
            task['completed'] = True
            break
    tasks.save_tasks(tasks_list)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task_web(task_id):
    """Удаляет задачу"""
    tasks_list = tasks.load_tasks()
    for i, task in enumerate(tasks_list):
        if task['id'] == task_id:
            tasks_list.pop(i)
            break
    # Перенумеровываем ID
    for idx, task in enumerate(tasks_list, 1):
        task['id'] = idx
    tasks.save_tasks(tasks_list)
    return redirect(url_for('index'))

@app.route('/statistics')
def statistics():
    """Страница со статистикой"""
    all_tasks = tasks.load_tasks()
    all_tasks = tasks.migrate_old_tasks(all_tasks)
    
    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t['completed'])
    pending = total - completed
    
    high_priority = sum(1 for t in all_tasks if t.get('priority') == 'high' and not t['completed'])
    medium_priority = sum(1 for t in all_tasks if t.get('priority') == 'medium' and not t['completed'])
    low_priority = sum(1 for t in all_tasks if t.get('priority') == 'low' and not t['completed'])
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    overdue = sum(1 for t in all_tasks if t.get('deadline') and t['deadline'] < today and not t['completed'])
    
    stats = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'progress': round(completed/total*100, 1) if total > 0 else 0,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'overdue': overdue
    }
    
    return render_template('statistics.html', stats=stats)

@app.route('/api/tasks')
def api_tasks():
    """JSON API для задач (для будущих мобильных приложений)"""
    all_tasks = tasks.load_tasks()
    return jsonify(all_tasks)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)