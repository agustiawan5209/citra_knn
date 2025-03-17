from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import DataLatih
from django import forms
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper


class LatihForm(forms.ModelForm):
    # nama = forms.CharField(max_length=30, min_length=5)
    # image = forms.ImageField()
    # kelas = forms.CharField(max_length=30)
    
    def __init__(self, *args, **kwargs) -> None:
        super(LatihForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        
    class Meta:
        model = DataLatih
        fields = ('nama', 'image', 'kelas')
        help_texts = {
            "nama": 'Isikan Nama File Dari Model Data Latih',
            "image": 'Masukkan image dengan extension image .jpg atau .png'
        }
        error_messages = {
            'name': {
                'required': 'Nama image harus diisi',
            },
            'image': {
                'required': 'image harus diisi',
            },
        }
    
    