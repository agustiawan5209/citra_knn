from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.conf.global_settings import LANGUAGE_CODE
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, 
                             help_text='Alamat email Anda',
                             error_messages={'required': 'Alamat email harus diisi',
                                             'invalid': 'Alamat email tidak valid'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.fields['password1'].help_text =  '<li>Password Harus Lebih dari 8 huruf</li>'
        self.fields['password2'].help_text =  '<span>Masukkan Ulang Password Anda</span>'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Berikan permissions staff secara default
        # user.user_permissions.set([
        #     'galeriapp.add_datauji',
        #     'galeriapp.delete_datauji',
        #     'galeriapp.change_datauji',
        #     'galeriapp.view_datauji',
        # ])
        if commit:
            user.save()
        return user
        # self.helper.layout = Layout(
        #     Row(Column(email)),
        # )
        
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
        help_texts = {
            'username': 'Nama pengguna Anda',
            'password1': ['Kata sandi Anda'],
            'password2': 'Konfirmasi kata sandi Anda',
        }
        
        error_messages = {
            'username': {
                'required': 'Nama pengguna harus diisi',
                'unique': 'Nama pengguna sudah digunakan',
            },
            'password1': {
                'required': 'Kata sandi harus diisi',
                'min_length': 'Kata sandi minimal 8 karakter',
            },
            'password2': {
                'required': 'Konfirmasi kata sandi harus diisi',
            },
        }
        
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('username', placeholder="username"),
            Field('password', placeholder="password"),)
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        