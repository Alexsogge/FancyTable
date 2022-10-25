from .models import *
from django.forms import ModelForm

class ConfigEntryForm(ModelForm):
    class Meta:
        model = ConfigEntry
        fields = ['extension', 'config_key', 'config_value']