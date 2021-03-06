from http import HTTPStatus

from django.test import Client, TestCase


class PromocodeURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_promocode_url_allowed_method(self):
        '''
        POST запрос на эндпоинт /generate/.
        '''
        response = self.client.post('/generate/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_generate_promocode_url_method_not_allowed(self):
        '''
        GET запрос на эндпоинт /generate/.
        '''
        response = self.client.get('/generate/')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_check_promocode_url_allowed_method(self):
        '''
        GET запрос на эндпоинт /check/.
        '''
        response = self.client.get('/check/')
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_check_promocode_url_method_not_allowed(self):
        '''
        POST запрос на эндпоинт /check/.
        '''
        response = self.client.post('/check/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
