"""
Тесты для калькулятора.
"""

import unittest
import tempfile
import os
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Тесты для класса Calculator."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        # Создаем временный файл для истории
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Создаем калькулятор с временным файлом истории
        self.calc = Calculator()
        self.calc.history_file = self.temp_file.name
        self.calc.history = []
    
    def tearDown(self):
        """Очистка после каждого теста."""
        # Удаляем временный файл
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add(self):
        """Тест сложения."""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
        
        result = self.calc.add(-1, 1)
        self.assertEqual(result, 0)
        
        result = self.calc.add(0.5, 0.5)
        self.assertEqual(result, 1.0)
    
    def test_subtract(self):
        """Тест вычитания."""
        result = self.calc.subtract(5, 3)
        self.assertEqual(result, 2)
        
        result = self.calc.subtract(1, 1)
        self.assertEqual(result, 0)
        
        result = self.calc.subtract(-1, 1)
        self.assertEqual(result, -2)
    
    def test_multiply(self):
        """Тест умножения."""
        result = self.calc.multiply(2, 3)
        self.assertEqual(result, 6)
        
        result = self.calc.multiply(-2, 3)
        self.assertEqual(result, -6)
        
        result = self.calc.multiply(0, 5)
        self.assertEqual(result, 0)
    
    def test_divide(self):
        """Тест деления."""
        result = self.calc.divide(6, 2)
        self.assertEqual(result, 3)
        
        result = self.calc.divide(5, 2)
        self.assertEqual(result, 2.5)
        
        result = self.calc.divide(-6, 2)
        self.assertEqual(result, -3)
    
    def test_divide_by_zero(self):
        """Тест деления на ноль."""
        with self.assertRaises(ValueError):
            self.calc.divide(5, 0)
    
    def test_history_after_operations(self):
        """Тест истории после операций."""
        # Выполняем несколько операций
        self.calc.add(2, 3)
        self.calc.subtract(5, 1)
        self.calc.multiply(4, 2)
        
        # Проверяем историю
        history = self.calc.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], ("2 + 3", 5))
        self.assertEqual(history[1], ("5 - 1", 4))
        self.assertEqual(history[2], ("4 * 2", 8))
    
    def test_clear_history(self):
        """Тест очистки истории."""
        # Добавляем операции
        self.calc.add(1, 1)
        self.calc.multiply(2, 3)
        
        # Проверяем, что история не пустая
        self.assertEqual(len(self.calc.get_history()), 2)
        
        # Очищаем историю
        self.calc.clear_history()
        
        # Проверяем, что история пустая
        self.assertEqual(len(self.calc.get_history()), 0)
    
    def test_history_persistence(self):
        """Тест сохранения истории в файл."""
        # Добавляем операции
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        
        # Создаем новый калькулятор с тем же файлом
        new_calc = Calculator()
        new_calc.history_file = self.temp_file.name
        new_calc.history = new_calc._load_history()
        
        # Проверяем, что история загрузилась
        history = new_calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], ("1 + 2", 3))
        self.assertEqual(history[1], ("3 * 4", 12))


if __name__ == '__main__':
    unittest.main()
