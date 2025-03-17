from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.dasboard, name='dashboard'),
    path('/chart-data/', views.chart_data, name='chart-data'),
]
