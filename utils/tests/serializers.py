from rest_framework.serializers import ModelSerializer
from .models import DummyModel


class AbstractModelSerializer(ModelSerializer):
    class Meta:
        abstract = True


class DummyModelSerializer(AbstractModelSerializer):
    class Meta:
        model = DummyModel
        fields = ('first_name', 'last_name', )
