from django.db import models
from django.contrib.auth.models import User
from flt.apps.current_user import registration
class CurrentUserField(models.ForeignKey):
    def __init__(self, **kwargs):
        #kwargs['related_name'] = 'random_related_name'
        super(CurrentUserField, self).__init__(User, null=True, **kwargs)

    def contribute_to_class(self, cls, name):
        super(CurrentUserField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry()
        registry.add_field(cls, self)