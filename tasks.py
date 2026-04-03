# tasks.py - Версия 1.1.0
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    """Загружает задачи из файла"""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    """Сохраняет задачи в файл"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task():
    """Добавляет новую задачу с дедлайном и приоритетом"""
    description = input("📝 Введи задачу: ")
    
    # Выбор приоритета
    print("\nПриоритеты:")
    print("1. 🔴 Высокий")
    print("2. 🟡 Средний")
    print("3. 🟢 Низкий")
    priority_choice = input("Твой выбор (1-3): ")
    
    priority_map = {"1": "high", "2": "medium", "3": "low"}
    priority = priority_map.get(priority_choice, "medium")
    
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    
    # Дедлайн
    deadline = input("📅 Дедлайн (ГГГГ-ММ-ДД) или Enter если нет: ")
    
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'completed': False,
        'priority': priority,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'deadline': deadline if deadline else None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Задача добавлена! {priority_emoji[priority]}")

def list_tasks(show_all=True):
    """Показывает все задачи, отсортированные по приоритету и дедлайну"""
    tasks = load_tasks()
    if not tasks:
        print("📭 Нет задач. Отдыхаем!")
        return
    
    # Сортировка: сначала высокий приоритет, потом по дедлайну
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda x: (priority_order.get(x['priority'], 2), x['deadline'] if x['deadline'] else "9999-12-31"))
    
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    
    print("\n" + "="*60)
    print("📋 МОЙ СПИСОК ЗАДАЧ")
    print("="*60)
    
    for task in tasks:
        if not show_all and task['completed']:
            continue
            
        status = "✅" if task['completed'] else "⭕"
        priority_icon = priority_emoji.get(task['priority'], "🟡")
        
        print(f"{status} {priority_icon} [{task['id']}] {task['description']}")
        print(f"   📅 Создана: {task['created_at']}")
        
        if task.get('deadline'):
            deadline_status = ""
            today = datetime.now().strftime("%Y-%m-%d")
            if task['deadline'] < today and not task['completed']:
                deadline_status = " ⚠️ ПРОСРОЧЕНА!"
            print(f"   ⏰ Дедлайн: {task['deadline']}{deadline_status}")
    
    print("="*60 + "\n")

def show_statistics():
    """Показывает статистику по задачам"""
    tasks = load_tasks()
    if not tasks:
        print("📭 Нет данных для статистики")
        return
    
    total = len(tasks)
    completed = sum(1 for t in tasks if t['completed'])
    pending = total - completed
    
    high_priority = sum(1 for t in tasks if t.get('priority') == 'high' and not t['completed'])
    overdue = sum(1 for t in tasks if t.get('deadline') and t['deadline'] < datetime.now().strftime("%Y-%m-%d") and not t['completed'])
    
    print("\n" + "="*50)
    print("📊 СТАТИСТИКА")
    print("="*50)
    print(f"📌 Всего задач: {total}")
    print(f"✅ Выполнено: {completed}")
    print(f"⏳ Осталось: {pending}")
    print(f"🔴 Срочных задач: {high_priority}")
    print(f"⚠️ Просроченных: {overdue}")
    print(f"📈 Прогресс: {round(completed/total*100, 1)}%" if total > 0 else "📈 Прогресс: 0%")
    print("="*50 + "\n")

def complete_task():
    """Отмечает задачу выполненной"""
    task_id = int(input("ID задачи для отметки: "))
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f"🎉 Выполнено: {task['description']}")
            return
    print(f"❌ Задача с ID {task_id} не найдена")

def delete_task():
    """Удаляет задачу"""
    task_id = int(input("ID задачи для удаления: "))
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            # Перенумеруем ID
            for idx, t in enumerate(tasks, 1):
                t['id'] = idx
            save_tasks(tasks)
            print(f"🗑️ Задача удалена")
            return
    print(f"❌ Задача с ID {task_id} не найдена")

def main():
    """Главное меню программы"""
    while True:
        print("\n" + "🚀"*15)
        print("   ТРЕКЕР ЗАДАЧ v1.1.0")
        print("🚀"*15)
        print("1. ➕ Добавить задачу")
        print("2. 📋 Показать все задачи")
        print("3. ✅ Отметить задачу выполненной")
        print("4. 📊 Статистика")
        print("5. 🗑️ Удалить задачу")
        print("6. 🚪 Выйти")
        
        choice = input("\nТвой выбор: ")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            show_statistics()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("👋 Пока! Хорошего дня!")
            break
        else:
            print("⚠️ Непонятная команда. Попробуй 1-6")

if __name__ == "__main__":
    main()