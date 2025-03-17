from django.urls import path, include
from . import views
urlpatterns = [
    path('', view=views.dataset_list, name='dataset_list'),
    path('create', view=views.dataset_create, name='dataset_create'),
    path('update/<int:pk>/', view=views.dataset_update, name='dataset_update'),
    path('delete/<int:pk>/', view=views.dataset_delete, name='dataset_delete'),
    path('upload_csv', view=views.upload_csv, name='upload_csv'),
]
