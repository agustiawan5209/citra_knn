from django import forms
from .models import Kelas
from crispy_forms.helper import FormHelper

class KelasForm(forms.ModelForm):
    nama = forms.CharField(max_length=50,error_messages={'required': 'Nama harus diisi'})
    informasi = forms.CharField(error_messages={'required': 'Informasi harus diisi'})
    
    def __init__(self, *args, **kwargs):
        super(KelasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
    
    # def save(self, commit=True):
    #     return super().save(commit=commit)
    class Meta:
        model = Kelas
        fields = ['nama', 'informasi']
        help_texts = {
            "nama": 'Masukkan Nama Kelas Dari Jenis Tanaman Obat',
        }
        
    
    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if Kelas.objects.filter(nama=nama).exists():
            raise forms.ValidationError("Nama ini sudah digunakan. Harap pilih nama yang lain.")
        return nama