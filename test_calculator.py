"""
Тесты для калькулятора в формате pytest.
"""

import pytest
import tempfile
from calculator import Calculator


@pytest.fixture
def calculator():
    """Фикстура для создания калькулятора с временным файлом истории."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as temp_file:
        # Создаем калькулятор с временным файлом истории
        calc = Calculator()
        calc.history_file = temp_file.name
        calc.history = []

        yield calc


@pytest.mark.parametrize("a,b,expected", [(2, 3, 5), (-1, 1, 0), (0.5, 0.5, 1.0)])
def test_add(calculator, a, b, expected):
    """Тест сложения с параметризацией."""
    assert calculator.add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(5, 3, 2), (1, 1, 0), (-1, 1, -2)])
def test_subtract(calculator, a, b, expected):
    """Тест вычитания с параметризацией."""
    assert calculator.subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(2, 3, 6), (-2, 3, -6), (0, 5, 0)])
def test_multiply(calculator, a, b, expected):
    """Тест умножения с параметризацией."""
    assert calculator.multiply(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(6, 2, 3), (5, 2, 2.5), (-6, 2, -3)])
def test_divide(calculator, a, b, expected):
    """Тест деления с параметризацией."""
    assert calculator.divide(a, b) == expected


def test_divide_by_zero(calculator):
    """Тест деления на ноль."""
    with pytest.raises(ValueError, match="Деление на ноль невозможно"):
        calculator.divide(5, 0)


def test_history_after_operations(calculator):
    """Тест истории после операций."""
    # Выполняем несколько операций
    calculator.add(2, 3)
    calculator.subtract(5, 1)
    calculator.multiply(4, 2)

    # Проверяем историю
    history = calculator.get_history()
    assert len(history) == 3
    assert history[0] == ("2 + 3", 5)
    assert history[1] == ("5 - 1", 4)
    assert history[2] == ("4 * 2", 8)


def test_clear_history(calculator):
    """Тест очистки истории."""
    # Добавляем операции
    calculator.add(1, 1)
    calculator.multiply(2, 3)

    # Проверяем, что история не пустая
    assert len(calculator.get_history()) == 2

    # Очищаем историю
    calculator.clear_history()

    # Проверяем, что история пустая
    assert len(calculator.get_history()) == 0


def test_history_persistence(calculator):
    """Тест сохранения истории в файл."""
    # Добавляем операции
    calculator.add(1, 2)
    calculator.multiply(3, 4)

    # Создаем новый калькулятор с тем же файлом
    new_calc = Calculator()
    new_calc.history_file = calculator.history_file
    new_calc.history = new_calc._load_history()

    # Проверяем, что история загрузилась
    history = new_calc.get_history()
    assert len(history) == 2
    assert history[0] == ("1 + 2", 3)
    assert history[1] == ("3 * 4", 12)
