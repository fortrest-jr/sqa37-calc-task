"""
Простой калькулятор с базовыми математическими операциями и историей вычислений.
"""

from typing import List, Tuple
import json
import os


class Calculator:
    """Калькулятор с базовыми математическими операциями."""
    
    def __init__(self):
        self.history_file = "calculator_history.json"
        self.history = self._load_history()
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел."""
        result = a + b
        self._add_to_history(f"{a} + {b}", result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание двух чисел."""
        result = a - b
        self._add_to_history(f"{a} - {b}", result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение двух чисел."""
        result = a * b
        self._add_to_history(f"{a} * {b}", result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Деление двух чисел."""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        result = a / b
        self._add_to_history(f"{a} / {b}", result)
        return result
    
    def get_history(self) -> List[Tuple[str, float]]:
        """Получить историю вычислений."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Очистить историю вычислений."""
        self.history = []
        self._save_history()
    
    def _add_to_history(self, operation: str, result: float) -> None:
        """Добавить операцию в историю."""
        self.history.append((operation, result))
        self._save_history()
    
    def _load_history(self) -> List[Tuple[str, float]]:
        """Загрузить историю из файла."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [(item['operation'], item['result']) for item in data]
            except (json.JSONDecodeError, KeyError):
                return []
        return []
    
    def _save_history(self) -> None:
        """Сохранить историю в файл."""
        data = [{'operation': op, 'result': res} for op, res in self.history]
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
