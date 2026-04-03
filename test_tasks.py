# test_tasks.py - Unit-тесты для трекера задач
import os
import pytest
import tasks

# 🔧 ФИКСТУРА: Создает временный файл для тестов
@pytest.fixture
def temp_tasks_file(tmp_path):
    """Создает временную папку для тестов, чтобы не трогать реальный tasks.json"""
    original_file = tasks.TASKS_FILE
    tasks.TASKS_FILE = str(tmp_path / "test_tasks.json")
    yield
    tasks.TASKS_FILE = original_file

# ============================================
# ТЕСТ 1: Миграция старых задач
# ============================================
def test_migrate_old_tasks():
    """Проверяет, что старые задачи получают priority и deadline"""
    old_tasks = [
        {'id': 1, 'description': 'Старая задача', 'completed': False, 'created_at': '2024-01-01'}
    ]
    
    migrated = tasks.migrate_old_tasks(old_tasks)
    
    assert 'priority' in migrated[0]
    assert 'deadline' in migrated[0]
    assert migrated[0]['priority'] == 'medium'
    assert migrated[0]['deadline'] is None

# ============================================
# ТЕСТ 2: Добавление задачи
# ============================================
def test_add_task(monkeypatch, temp_tasks_file):
    """Проверяет, что задача добавляется корректно"""
    inputs = iter(["Тестовая задача", "1", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    if os.path.exists(tasks.TASKS_FILE):
        os.remove(tasks.TASKS_FILE)
    
    tasks.add_task()
    
    tasks_list = tasks.load_tasks()
    assert len(tasks_list) == 1
    assert tasks_list[0]['description'] == "Тестовая задача"
    assert tasks_list[0]['priority'] == "high"

# ============================================
# ТЕСТ 3: Удаление задачи
# ============================================
def test_delete_task(temp_tasks_file):
    """Проверяет, что задача удаляется"""
    test_task = {'id': 1, 'description': 'Удалить меня', 'completed': False, 
                 'created_at': '2024-01-01', 'priority': 'medium', 'deadline': None}
    tasks.save_tasks([test_task])
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.input', lambda _: "1")
        tasks.delete_task()
    
    tasks_list = tasks.load_tasks()
    assert len(tasks_list) == 0

# ============================================
# ТЕСТ 4: Отметка задачи как выполненной
# ============================================
def test_complete_task(temp_tasks_file):
    """Проверяет, что задача отмечается выполненной"""
    test_task = {'id': 1, 'description': 'Сделать тест', 'completed': False,
                 'created_at': '2024-01-01', 'priority': 'high', 'deadline': None}
    tasks.save_tasks([test_task])
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.input', lambda _: "1")
        tasks.complete_task()
    
    tasks_list = tasks.load_tasks()
    assert tasks_list[0]['completed'] == True

# ============================================
# ТЕСТ 5: Загрузка из пустого файла
# ============================================
def test_load_empty_tasks(temp_tasks_file):
    """Проверяет, что при отсутствии файла возвращается пустой список"""
    if os.path.exists(tasks.TASKS_FILE):
        os.remove(tasks.TASKS_FILE)
    
    tasks_list = tasks.load_tasks()
    assert tasks_list == []

# ============================================
# ТЕСТ 6: Сохранение и загрузка задач
# ============================================
def test_save_and_load_tasks(temp_tasks_file):
    """Проверяет, что задачи сохраняются и загружаются корректно"""
    test_tasks = [
        {'id': 1, 'description': 'Задача 1', 'completed': False, 'priority': 'high', 'deadline': None, 'created_at': '2024-01-01'},
        {'id': 2, 'description': 'Задача 2', 'completed': True, 'priority': 'low', 'deadline': '2024-12-31', 'created_at': '2024-01-01'}
    ]
    
    tasks.save_tasks(test_tasks)
    loaded_tasks = tasks.load_tasks()
    
    assert loaded_tasks == test_tasks

# ============================================
# ТЕСТ 7: Удаление несуществующей задачи
# ============================================
def test_delete_nonexistent_task(temp_tasks_file, capsys):
    """Проверяет, что при удалении несуществующей задачи выводится ошибка"""
    test_task = {'id': 1, 'description': 'Существующая задача', 'completed': False,
                 'created_at': '2024-01-01', 'priority': 'medium', 'deadline': None}
    tasks.save_tasks([test_task])
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.input', lambda _: "99")
        tasks.delete_task()
    
    captured = capsys.readouterr()
    assert "не найдена" in captured.out

# ============================================
# ТЕСТ 8: Нумерация ID после удаления
# ============================================
def test_reindex_after_delete(temp_tasks_file):
    """Проверяет, что после удаления ID перенумеровываются"""
    tasks_list = [
        {'id': 1, 'description': 'Первая', 'completed': False, 'priority': 'medium', 'deadline': None, 'created_at': '2024-01-01'},
        {'id': 2, 'description': 'Вторая', 'completed': False, 'priority': 'medium', 'deadline': None, 'created_at': '2024-01-01'},
        {'id': 3, 'description': 'Третья', 'completed': False, 'priority': 'medium', 'deadline': None, 'created_at': '2024-01-01'}
    ]
    tasks.save_tasks(tasks_list)
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr('builtins.input', lambda _: "2")
        tasks.delete_task()
    
    remaining = tasks.load_tasks()
    assert len(remaining) == 2
    assert remaining[0]['id'] == 1
    assert remaining[1]['id'] == 2
    assert remaining[1]['description'] == "Третья"