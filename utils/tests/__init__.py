from django.db import connection
from django.db.models.base import ModelBase


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
