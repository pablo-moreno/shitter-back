from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import RelatedField


class PropertyRelatedField(RelatedField):
    """
        A read-write field that represents the target of the relationship
        by a unique 'property_field' attribute.

        All the credit to:
        https://stackoverflow.com/a/61815040
    """
    property_field = None
    default_error_messages = {
        'does_not_exist': _('Object with {property_field}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, **kwargs):
        assert self.property_field is not None, 'The `property_field` is required.'
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.property_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.property_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.property_field)


class UUIDRelatedField(PropertyRelatedField):
    property_field = 'uuid'


class UsernameRelatedField(PropertyRelatedField):
    property_field = 'username'
