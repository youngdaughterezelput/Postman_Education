import os
import requests
import unittest
from dotenv import load_dotenv # Для загрузки переменных из .env файла

# Загружаем переменные окружения из файла .env
load_dotenv()

class OptimizationAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Выполняется один раз перед запуском всех тестов в классе."""
        cls.base_url = os.getenv('BASE_URL')
        cls.organization_id = os.getenv('ORGANIZATION_ID')
        cls.auth_token = os.getenv('AUTH_TOKEN')

        if not all([cls.base_url, cls.organization_id, cls.auth_token]):
            raise ValueError("Необходимо установить переменные окружения: BASE_URL, ORGANIZATION_ID, AUTH_TOKEN")

        cls.endpoint = f"{cls.base_url}/restapi/v2/organizations/{cls.organization_id}/optimizations?overview=true"
        cls.headers = {
            'Authorization': f'Bearer {cls.auth_token}',
            # Добавьте другие необходимые заголовки, если они требуются API
            # 'Content-Type': 'application/json'
        }

    def setUp(self):
        """Выполняется перед каждым тестом."""
        # Выполняем запрос один раз и сохраняем результат для всех тестов
        if not hasattr(self, 'response'):
            self.response = requests.get(self.endpoint, headers=self.headers)

    def test_01_status_code(self):
        """Тест 1: Проверка успешного кода ответа"""
        self.assertEqual(self.response.status_code, 200,
                         f"Ожидаемый статус 200, получили {self.response.status_code}")

    def test_02_content_type(self):
        """Тест 2: Проверка заголовка Content-Type"""
        content_type = self.response.headers.get('Content-Type', '')
        self.assertIn('application/json', content_type,
                      f"Content-Type должен быть application/json, получили '{content_type}'")

    def test_03_response_structure(self):
        """Тест 3: Проверка структуры ответа (наличие ключевых полей)"""
        self.assertEqual(self.response.status_code, 200) # Убедимся, что запрос успешен
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        self.assertIsInstance(data, dict, "Тело ответа должно быть JSON объектом")

        expected_top_level_fields = [
            "abandoned_snapshots", "abandoned_instances", "obsolete_images",
            "instances_for_migration", "underutilized_instances", "unpaid_databases",
            "abandoned_object_storages", "abandoned_managed_databases", "abandoned_ip",
            "abandoned_resources", "abandoned_kubernetes_clusters", "instance_generation_upgrade",
            "abandoned_volumes", "short_living_instances", "dismissed_optimizations",
            "excluded_optimizations", "abandoned_users", "instance_sharding",
            "obsolete_snapshot_chains", "rightsizing_instances", "cloud_accounts"
        ]

        for field in expected_top_level_fields:
            self.assertIn(field, data, f"Ответ должен содержать поле '{field}'")

    def test_04_abandoned_instances_structure(self):
        """Тест 4: Проверка структуры конкретного раздела (пример abandoned_instances)"""
        self.assertEqual(self.response.status_code, 200)
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        section = data.get("abandoned_instances")
        self.assertIsNotNone(section, "Поле 'abandoned_instances' должно присутствовать")
        self.assertIsInstance(section, dict, "'abandoned_instances' должно быть объектом")

        self.assertIn('count', section, "Поле 'count' должно присутствовать в 'abandoned_instances'")
        self.assertIsInstance(section['count'], int, "'count' должно быть числом")

        self.assertIn('saving', section, "Поле 'saving' должно присутствовать в 'abandoned_instances'")
        # saving может быть int или float
        self.assertIsInstance(section['saving'], (int, float), "'saving' должно быть числом")

        self.assertIn('options', section, "Поле 'options' должно присутствовать в 'abandoned_instances'")
        self.assertIsInstance(section['options'], dict, "'options' должно быть объектом")

        options = section['options']
        self.assertIn('days_threshold', options, "Поле 'days_threshold' должно присутствовать в 'options'")
        self.assertIsInstance(options['days_threshold'], int, "'days_threshold' должно быть числом")
        self.assertIn('excluded_pools', options, "Поле 'excluded_pools' должно присутствовать в 'options'")
        self.assertIsInstance(options['excluded_pools'], dict, "'excluded_pools' должно быть объектом")
        self.assertIn('skip_cloud_accounts', options, "Поле 'skip_cloud_accounts' должно присутствовать в 'options'")
        self.assertIsInstance(options['skip_cloud_accounts'], list, "'skip_cloud_accounts' должно быть массивом")

        self.assertIn('items', section, "Поле 'items' должно присутствовать в 'abandoned_instances'")
        # items может быть массивом или null
        self.assertTrue(isinstance(section['items'], list) or section['items'] is None,
                        "'items' должно быть массивом или null")

    def test_05_abandoned_instance_item_structure(self):
        """Тест 5: Проверка структуры элемента в разделе (пример abandoned_instances.items[0])"""
        self.assertEqual(self.response.status_code, 200)
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        items = data.get("abandoned_instances", {}).get("items")
        if items and isinstance(items, list) and len(items) > 0:
            first_item = items[0]
            self.assertIsInstance(first_item, dict, "Элемент в 'items' должен быть объектом")

            # Проверяем обязательные или часто встречающиеся поля
            # resource_name и resource_id могут быть null, поэтому проверяем тип или None
            self.assertTrue(first_item.get('resource_name') is None or isinstance(first_item.get('resource_name'), str),
                            "'resource_name' должно быть строкой или null")
            self.assertTrue(first_item.get('resource_id') is None or isinstance(first_item.get('resource_id'), str),
                            "'resource_id' должно быть строкой или null")

            self.assertIn('cloud_account_id', first_item, "Поле 'cloud_account_id' должно присутствовать")
            self.assertIsInstance(first_item['cloud_account_id'], str, "'cloud_account_id' должно быть строкой")

            self.assertIn('cloud_type', first_item, "Поле 'cloud_type' должно присутствовать")
            self.assertIsInstance(first_item['cloud_type'], str, "'cloud_type' должно быть строкой")

            self.assertIn('cloud_account_name', first_item, "Поле 'cloud_account_name' должно присутствовать")
            self.assertIsInstance(first_item['cloud_account_name'], str, "'cloud_account_name' должно быть строкой")

            # region может быть null
            self.assertTrue(first_item.get('region') is None or isinstance(first_item.get('region'), str),
                            "'region' должно быть строкой или null")

            self.assertIn('saving', first_item, "Поле 'saving' должно присутствовать")
            self.assertIsInstance(first_item['saving'], (int, float), "'saving' должно быть числом")

            self.assertIn('detected_at', first_item, "Поле 'detected_at' должно присутствовать")
            self.assertIsInstance(first_item['detected_at'], int, "'detected_at' должно быть числом")

            # Проверим, что detected_at выглядит как разумный unix timestamp
            # (после 2020 года ~1577836800, не в будущем)
            detected_at = first_item['detected_at']
            self.assertGreater(detected_at, 1577836800, "'detected_at' должен быть после 2020 года")
            import time
            now_plus_buffer = int(time.time()) + 86400 # + 1 день допуск
            self.assertLessEqual(detected_at, now_plus_buffer, "'detected_at' не должно быть в далеком будущем")

        else:
            # Если items пустой или null, проверим count
            count = data.get("abandoned_instances", {}).get("count", -1)
            # self.assertIsNone(items) # или items == []
            self.assertEqual(count, 0 if items == [] else count, # Простая проверка логики
                             "Если items отсутствует или пустой, count обычно 0 или соответствует")

    def test_06_cloud_accounts_structure(self):
        """Тест 6: Проверка структуры раздела cloud_accounts"""
        self.assertEqual(self.response.status_code, 200)
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        accounts = data.get("cloud_accounts")
        self.assertIsInstance(accounts, list, "'cloud_accounts' должно быть массивом")

        if accounts: # Проверяем только если массив не пуст
            first_account = accounts[0]
            self.assertIsInstance(first_account, dict, "Элемент в 'cloud_accounts' должен быть объектом")

            self.assertIn('id', first_account, "Поле 'id' должно присутствовать в аккаунте")
            self.assertIsInstance(first_account['id'], str, "'id' аккаунта должно быть строкой")

            self.assertIn('name', first_account, "Поле 'name' должно присутствовать в аккаунте")
            self.assertIsInstance(first_account['name'], str, "'name' аккаунта должно быть строкой")

            self.assertIn('type', first_account, "Поле 'type' должно присутствовать в аккаунте")
            self.assertIsInstance(first_account['type'], str, "'type' аккаунта должно быть строкой")
            # Можно добавить проверку на допустимые значения типа
            valid_types = ['aws_cnr', 'gcp_cnr', 'azure_cnr', 'alibaba_cnr']
            self.assertIn(first_account['type'], valid_types,
                          f"'type' аккаунта должно быть одним из {valid_types}")

    def test_07_data_consistency(self):
        """Тест 7: Проверка согласованности данных (пример: суммарные значения)"""
        self.assertEqual(self.response.status_code, 200)
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        section = data.get("abandoned_instances")
        if section and isinstance(section, dict):
            items = section.get("items")
            count = section.get("count")
            if items is not None and isinstance(items, list): # Проверяем только если items не null
                self.assertEqual(len(items), count,
                                 f"Количество элементов в 'items' ({len(items)}) должно соответствовать 'count' ({count})")
            # Примечание: Проверка суммы 'saving' сложнее без полных данных items.

    def test_08_error_handling(self):
        """Тест 8: Проверка обработки ошибок (пример: внутренняя ошибка сервера в секции)"""
        # Этот тест проверяет наличие ошибок *внутри* структуры ответа, а не HTTP ошибок.
        # Например, ошибка в секции instance_generation_upgrade
        self.assertEqual(self.response.status_code, 200)
        try:
            data = self.response.json()
        except requests.exceptions.JSONDecodeError:
            self.fail("Ответ не является валидным JSON")

        section = data.get("instance_generation_upgrade")
        if section and isinstance(section, dict) and 'error' in section:
            # Проверяем, что если поле error присутствует, оно является строкой
            self.assertIsInstance(section['error'], str, "Поле 'error' в секции должно быть строкой")
            # Проверяем часть сообщения об ошибке из примера данных
            self.assertIn("500 Server Error", section['error'],
                          "Сообщение об ошибке должно содержать '500 Server Error'")

    # --- Тесты для негативных сценариев ---
    # Эти тесты требуют отдельных методов или параметризации, так как используют разные URL/заголовки

    def test_99_status_401_unauthorized(self):
        """Тест: Проверка кода 401 для неавторизованного запроса"""
        # Создаем новый запрос без токена авторизации
        headers_no_auth = {k: v for k, v in self.headers.items() if k != 'Authorization'}
        response_unauth = requests.get(self.endpoint, headers=headers_no_auth)

        self.assertEqual(response_unauth.status_code, 401,
                         f"Ожидаемый статус 401 для неавторизованного запроса, получили {response_unauth.status_code}")
        # Можно добавить проверку структуры тела ошибки, если API возвращает её

    # def test_status_404_not_found(self):
    #     """Тест: Проверка кода 404 для несуществующей организации"""
    #     # Создаем новый запрос с неверным organization_id
    #     invalid_org_id = "00000000-0000-0000-0000-000000000000"
    #     invalid_endpoint = f"{self.base_url}/restapi/v2/organizations/{invalid_org_id}/optimizations?overview=true"
    #     response_not_found = requests.get(invalid_endpoint, headers=self.headers)
    #
    #     self.assertEqual(response_not_found.status_code, 404,
    #                      f"Ожидаемый статус 404 для неверного organization_id, получили {response_not_found.status_code}")
    #     # Можно добавить проверку структуры тела ошибки

if __name__ == '__main__':
    # Запуск тестов
    unittest.main(verbosity=2) # verbosity=2 для более подробного вывода