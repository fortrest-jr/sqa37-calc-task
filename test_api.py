"""
Тесты для API калькулятора.
"""

import pytest
import json
import tempfile
import os
from app import app, calculator


@pytest.fixture
def client():
    """Создание тестового клиента Flask."""
    # Создаем временный файл для истории
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()

    # Настраиваем тестовое окружение
    app.config['TESTING'] = True
    calculator.history_file = temp_file.name
    calculator.history = []

    with app.test_client() as client:
        yield client

    # Очищаем временный файл
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


class TestCalculatorAPI:
    """Тесты для API калькулятора."""

    def test_health_check(self, client):
        """Тест проверки работоспособности API."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert 'Калькулятор работает' in data['message']

    def test_add_operation(self, client):
        """Тест операции сложения."""
        response = client.post('/api/add', data=json.dumps({'a': 2, 'b': 3}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'add'
        assert data['a'] == 2
        assert data['b'] == 3
        assert data['result'] == 5

    def test_subtract_operation(self, client):
        """Тест операции вычитания."""
        response = client.post('/api/subtract', data=json.dumps({'a': 5, 'b': 3}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'subtract'
        assert data['a'] == 5
        assert data['b'] == 3
        assert data['result'] == 2

    def test_multiply_operation(self, client):
        """Тест операции умножения."""
        response = client.post('/api/multiply', data=json.dumps({'a': 4, 'b': 3}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'multiply'
        assert data['a'] == 4
        assert data['b'] == 3
        assert data['result'] == 12

    def test_divide_operation(self, client):
        """Тест операции деления."""
        response = client.post('/api/divide', data=json.dumps({'a': 6, 'b': 2}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'divide'
        assert data['a'] == 6
        assert data['b'] == 2
        assert data['result'] == 3

    def test_divide_by_zero(self, client):
        """Тест деления на ноль."""
        response = client.post('/api/divide', data=json.dumps({'a': 5, 'b': 0}), content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Деление на ноль невозможно' in data['error']

    def test_missing_parameters(self, client):
        """Тест отсутствующих параметров."""
        response = client.post('/api/add', data=json.dumps({'a': 2}), content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Требуются параметры a и b' in data['error']

    def test_invalid_json(self, client):
        """Тест некорректного JSON."""
        response = client.post('/api/add', data='invalid json', content_type='application/json')
        assert response.status_code == 400

    def test_universal_calculate_endpoint(self, client):
        """Тест универсального endpoint для вычислений."""
        # Тест сложения
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': 'add', 'a': 1, 'b': 2}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 3

        # Тест вычитания
        response = client.post(
            '/api/calculate',
            data=json.dumps({'operation': 'subtract', 'a': 5, 'b': 2}),
            content_type='application/json',
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 3

    def test_invalid_operation(self, client):
        """Тест неподдерживаемой операции."""
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': 'power', 'a': 2, 'b': 3}), content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Неподдерживаемая операция' in data['error']

    def test_history_endpoints(self, client):
        """Тест работы с историей."""
        # Выполняем несколько операций
        client.post('/api/add', data=json.dumps({'a': 1, 'b': 2}), content_type='application/json')
        client.post('/api/multiply', data=json.dumps({'a': 3, 'b': 4}), content_type='application/json')

        # Получаем историю
        response = client.get('/api/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 2
        assert len(data['history']) == 2
        assert data['history'][0]['operation'] == '1 + 2'
        assert data['history'][0]['result'] == 3
        assert data['history'][1]['operation'] == '3 * 4'
        assert data['history'][1]['result'] == 12

        # Очищаем историю
        response = client.delete('/api/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'История очищена' in data['message']

        # Проверяем, что история пуста
        response = client.get('/api/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
        assert len(data['history']) == 0

    def test_404_error(self, client):
        """Тест обработки 404 ошибки."""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'Endpoint не найден' in data['error']

    def test_method_not_allowed(self, client):
        """Тест обработки 405 ошибки."""
        response = client.get('/api/add')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'Метод не поддерживается' in data['error']


if __name__ == '__main__':
    pytest.main([__file__])
