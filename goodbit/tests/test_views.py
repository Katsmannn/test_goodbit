import os.path
import shutil
import tempfile

from django.conf import settings
from django.test import Client, TestCase, override_settings


TEMP_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
TEMP_JSON_FILE = TEMP_ROOT + '/tmp_promocodes.json'


@override_settings(FILE_PATH=TEMP_JSON_FILE)
class PromocodeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        groups = ['group1', 'group2', 'group3']
        amounts = range(1, 21)
        cls.correct_data = [
            {
                'group': f'{group}',
                'amount': amount
            } for group in groups for amount in amounts
        ]
        cls.not_correct_data = [{}, {'group': 'group'}, {'amount': 9}]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_generate_promocode_not_correct_data(self):
        '''
        Тест запроса генерации промокода с неполными параметрами.
        В запросе отсутствуют поля group или amount.
        '''
        response = self.client.post('/generate/', self.not_correct_data[0])
        self.assertEqual(
            response.data, 'Отсутствуют обязательные параметры group и amount'
        )

    def test_check_promocode_not_correct_data(self):
        '''
        Тест запроса проверки промокода с неполными параметрами.
        В запросе отсутствует поле code.
        '''
        response = self.client.post('/check/')
        self.assertEqual(
            response.data, 'Отсутствует обязательный параметр code'
        )

    def test_generate_promocode_correct_data(self):
        '''
        Тест ответа при корректном запросе генерации промокода.
        '''
        response = self.client.post('/generate/', self.correct_data[0])
        is_file_created = os.path.exists(settings.FILE_PATH)
        self.assertIsNotNone(
            response.data.get('code')
        )
        self.assertTrue(is_file_created)

    def test_check_promocode_correct_data(self):
        '''
        Тест ответа при запросе проверки промокода.
        '''
        data = self.correct_data[0]
        group = data.get('group')
        code = self.client.post('/generate/', data).data.get('code')
        check_code = self.client.post('/check/', data={'code': code}).data
        self.assertEqual(check_code, f"Код существует. Группа - {group}.")
