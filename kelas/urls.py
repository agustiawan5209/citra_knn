from django.urls import path
from . import views

urlpatterns = [
    path('', views.kelas_list, name='kelas_list'),
    path('tambah/', views.kelas_create, name='kelas_create'),
    path('ubah/<int:pk>/', views.kelas_update, name='kelas_update'),
    path('delete/<int:pk>/', views.kelas_delete, name='kelas_delete'),
]