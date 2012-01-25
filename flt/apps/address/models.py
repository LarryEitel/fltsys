from django.db import models
import flt.apps.common.models

# Create your models here.

class ContactModel(models.Model, flt.apps.common.models.AjaxModelHelper):
	email = models.EmailField()
	first = models.CharField(max_length=100)
	last = models.CharField(max_length=100)
