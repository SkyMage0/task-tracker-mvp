# tasks.py - Главный файл приложения
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

def add_task(description):
    """Добавляет новую задачу"""
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Задача добавлена: {description}")

def list_tasks():
    """Показывает все задачи"""
    tasks = load_tasks()
    if not tasks:
        print("📭 Нет задач. Отдыхаем!")
        return
    
    print("\n" + "="*50)
    print("📋 МОЙ СПИСОК ЗАДАЧ")
    print("="*50)
    for task in tasks:
        status = "✅" if task['completed'] else "⭕"
        print(f"{status} [{task['id']}] {task['description']}")
        print(f"   📅 {task['created_at']}")
    print("="*50 + "\n")

def complete_task(task_id):
    """Отмечает задачу выполненной"""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f"🎉 Задача выполнена: {task['description']}")
            return
    print(f"❌ Задача с ID {task_id} не найдена")

def main():
    """Главное меню программы"""
    while True:
        print("\n" + "🚀"*10)
        print("   ТРЕКЕР ЗАДАЧ")
        print("🚀"*10)
        print("1. ➕ Добавить задачу")
        print("2. 📋 Показать все задачи")
        print("3. ✅ Отметить задачу выполненной")
        print("4. 🚪 Выйти")
        
        choice = input("\nТвой выбор: ")
        
        if choice == '1':
            desc = input("Введи задачу: ")
            add_task(desc)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = int(input("ID задачи для отметки: "))
            complete_task(task_id)
        elif choice == '4':
            print("👋 Пока! Хорошего дня!")
            break
        else:
            print("⚠️ Непонятная команда. Попробуй 1, 2, 3 или 4")

if __name__ == "__main__":
    main()