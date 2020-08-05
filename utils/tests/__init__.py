from django.db import connection
from django.db.models.base import ModelBase
from django.urls import reverse


class DummyModelTestCaseMixin(object):
    dummy_models = []
    base_dummy_models = []

    def __install_dummy_models__(self):
        for model in self.dummy_models:
            model_base = ModelBase(
                '__DummyModel__' + model.__name__, (model, ), {'__module__': model.__module__}
            )
            self.base_dummy_models.append(model_base)

            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(model_base)

    def tearDown(self):
        for model_base in self.base_dummy_models:
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(model_base)


class AuthTestCaseMixin(object):
    def perform_authentication(self, username, password):
        response = self.client.post(reverse('authentication:login'), {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        self.auth_token = response.json().get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.auth_token}')
