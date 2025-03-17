from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'crud-datauji', views.DataUjiViewSet, basename='crud_datauji')

urlpatterns = [
    path('api/', include(router.urls)),
    path('predict_image/', views.PredictImageView.as_view()),
    
    path('', views.datauji_list, name='datauji_list'),
    path('delete/<int:pk>/', views.datauji_delete, name='datauji_delete'),
]
