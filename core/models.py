from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from current_user import registration
from django_extensions.db.models import TimeStampedModel
from current_user.models import CurrentUserField

class Property:
    def __init__(self, **kwd):
        for (key, val) in kwd.iteritems():
            if isinstance(val, dict):  val = Property(**val)
            self.__dict__[key] = val

    @property
    def p_django_field_choices(self):
        return [(v, k) for (k, v) in self.__dict__.items()]
    
class CurrentUserField(models.ForeignKey):
    def __init__(self, **kwargs):
        #kwargs['related_name'] = 'random_related_name'
        super(CurrentUserField, self).__init__(User, null=True, **kwargs)

    def contribute_to_class(self, cls, name):
        super(CurrentUserField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry()
        registry.add_field(cls, self)
        

class MyModel(TimeStampedModel):
    class Meta:
        abstract = True
