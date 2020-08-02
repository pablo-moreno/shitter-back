from random import choice
from string import digits, ascii_letters
from .models import DummyModel
from .serializers import DummyModelSerializer
from rest_framework.test import APITestCase, APIClient
from utils.http import HttpService

from . import DummyModelTestCaseMixin


class DummyModelService(HttpService):
    model = DummyModel
    serializer_class = DummyModelSerializer
    api_url = '/api'
    authorization_header = 'Token'
    authorization_header_name = 'X-Auth'
    default_http_client = APIClient()


class TestHttpService(APITestCase, DummyModelTestCaseMixin):
    dummy_models = (DummyModel, )

    def setUp(self) -> None:
        self.__install_dummy_models__()

        self.http_service = DummyModelService()
        self.token = ''.join(choice(digits + ascii_letters) for _ in range(32))
        self.http_service.set_token(self.token)

    def test_http_service_model_slug(self):
        self.assertEqual(self.http_service.get_model_slug(), 'dummy-models')

    def test_http_service_get_token(self):
        self.assertEqual(self.http_service.get_token(), self.token)

    def test_http_service_get_headers(self):
        expected_headers = {
            DummyModelService.authorization_header_name: f'{DummyModelService.authorization_header} {self.token}',
        }
        self.assertEqual(self.http_service.get_headers(), expected_headers)
