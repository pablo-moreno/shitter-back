from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import RelatedField


class UUIDRelatedField(RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'slug' attribute.

    All the credit to:
    https://stackoverflow.com/a/61815040
    """
    default_error_messages = {
        'does_not_exist': _('Object with {uuid_field}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, uuid_field='uuid', **kwargs):
        assert uuid_field is not None, 'The `uuid_field` argument is required.'
        self.uuid_field = uuid_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.uuid_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.uuid_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.uuid_field)
