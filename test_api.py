"""
Тесты для API калькулятора.
"""

import pytest
import json
import tempfile
from app import app, calculator


@pytest.fixture
def client():
    """Создание тестового клиента Flask с изолированной историей."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as temp_file:
        # Настраиваем тестовое окружение
        app.config['TESTING'] = True
        calculator.history_file = temp_file.name

        # Очищаем историю перед каждым тестом
        calculator.history = []

        with app.test_client() as client:
            yield client


class TestCalculatorAPI:
    """Тесты для API калькулятора."""

    def test_health_check(self, client):
        """Тест проверки работоспособности API."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
        assert 'Калькулятор работает' in data['message']

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 5),  # положительные числа
            (-1, 5, 4),  # отрицательное и положительное
            (0, 0, 0),  # нули
            (999999, 1, 1000000),  # большие числа
            (-5, -3, -8),  # отрицательные числа
        ],
    )
    def test_add_operation(self, client, a, b, expected):
        """Тест операции сложения с различными параметрами."""
        response = client.post('/api/add', data=json.dumps({'a': a, 'b': b}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'add'
        assert data['a'] == a
        assert data['b'] == b
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (5, 3, 2),  # положительные числа
            (5, -3, 8),  # вычитание отрицательного
            (0, 0, 0),  # нули
            (1000000, 1, 999999),  # большие числа
            (-5, -3, -2),  # отрицательные числа
        ],
    )
    def test_subtract_operation(self, client, a, b, expected):
        """Тест операции вычитания с различными параметрами."""
        response = client.post('/api/subtract', data=json.dumps({'a': a, 'b': b}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'subtract'
        assert data['a'] == a
        assert data['b'] == b
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (4, 3, 12),  # положительные числа
            (-2, 5, -10),  # отрицательное и положительное
            (0, 100, 0),  # умножение на ноль
            (1000, 1000, 1000000),  # большие числа
            (-3, -4, 12),  # отрицательные числа
        ],
    )
    def test_multiply_operation(self, client, a, b, expected):
        """Тест операции умножения с различными параметрами."""
        response = client.post('/api/multiply', data=json.dumps({'a': a, 'b': b}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'multiply'
        assert data['a'] == a
        assert data['b'] == b
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (6, 2, 3),  # положительные числа
            (-10, 2, -5),  # отрицательное и положительное
            (0, 5, 0),  # деление нуля
            (1000000, 2, 500000),  # большие числа
            (-9, -3, 3),  # отрицательные числа
        ],
    )
    def test_divide_operation(self, client, a, b, expected):
        """Тест операции деления с различными параметрами."""
        response = client.post('/api/divide', data=json.dumps({'a': a, 'b': b}), content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['operation'] == 'divide'
        assert data['a'] == a
        assert data['b'] == b
        assert data['result'] == expected

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
        assert response.status_code == 500

    @pytest.mark.parametrize(
        "operation,a,b,expected", [('add', 1, 2, 3), ('add', -1, 5, 4), ('add', 0, 0, 0), ('add', 999999, 1, 1000000)]
    )
    def test_calculate_add_operation(self, client, operation, a, b, expected):
        """Тест операции сложения через универсальный endpoint."""
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': operation, 'a': a, 'b': b}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "operation,a,b,expected",
        [('subtract', 5, 2, 3), ('subtract', 5, -2, 7), ('subtract', 0, 0, 0), ('subtract', 1000000, 1, 999999)],
    )
    def test_calculate_subtract_operation(self, client, operation, a, b, expected):
        """Тест операции вычитания через универсальный endpoint."""
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': operation, 'a': a, 'b': b}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "operation,a,b,expected",
        [('multiply', 4, 3, 12), ('multiply', -2, 5, -10), ('multiply', 0, 100, 0), ('multiply', 1000, 1000, 1000000)],
    )
    def test_calculate_multiply_operation(self, client, operation, a, b, expected):
        """Тест операции умножения через универсальный endpoint."""
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': operation, 'a': a, 'b': b}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == expected

    @pytest.mark.parametrize(
        "operation,a,b,expected",
        [('divide', 6, 2, 3), ('divide', -10, 2, -5), ('divide', 0, 5, 0), ('divide', 1000000, 2, 500000)],
    )
    def test_calculate_divide_operation(self, client, operation, a, b, expected):
        """Тест операции деления через универсальный endpoint."""
        response = client.post(
            '/api/calculate', data=json.dumps({'operation': operation, 'a': a, 'b': b}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == expected

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
        assert data['history'][0]['operation'] == '1.0 + 2.0'
        assert data['history'][0]['result'] == 3
        assert data['history'][1]['operation'] == '3.0 * 4.0'
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

    def test_large_numbers(self, client):
        """Тест работы с очень большими числами."""
        # Максимальное 32-битное целое число
        max_int = 2**31 - 1
        response = client.post(
            '/api/add', data=json.dumps({'a': max_int, 'b': max_int}), content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == max_int * 2

    def test_invalid_data_types(self, client):
        """Тест некорректных типов данных."""
        response = client.post('/api/add', data=json.dumps({'a': 'string', 'b': 2}), content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'could not convert string to float' in data['error']

    def test_empty_request(self, client):
        """Тест пустого запроса."""
        response = client.post('/api/add', data='{}', content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Требуются параметры a и b' in data['error']


if __name__ == '__main__':
    pytest.main([__file__])
