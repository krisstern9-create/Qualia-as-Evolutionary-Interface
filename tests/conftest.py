"""
Conftest для pytest.

Автоматически добавляет корень проекта в sys.path
чтобы тесты могли импортировать модули.

Автор: Kris Stern
Лицензия: MIT
"""

import sys
import os
import pytest
from pathlib import Path


def pytest_configure(config):
    """
    Конфигурация pytest перед запуском тестов.
    
    Добавляет родительскую директорию в sys.path
    чтобы импорты работали корректно.
    """
    # Получаем корень проекта (родительская папка от tests/)
    root_dir = Path(__file__).parent.parent
    
    # Добавляем в sys.path если ещё не добавлен
    root_str = str(root_dir.resolve())
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    
    # Устанавливаем PYTHONPATH для subprocess
    os.environ['PYTHONPATH'] = root_str + ':' + os.environ.get('PYTHONPATH', '')


@pytest.fixture(scope='session')
def project_root():
    """Фикстура: путь к корню проекта."""
    return Path(__file__).parent.parent


@pytest.fixture(scope='session')
def tests_root():
    """Фикстура: путь к папке тестов."""
    return Path(__file__).parent
