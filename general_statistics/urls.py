from django.urls import path
from general_statistics import views


urlpatterns = [
    path('', views.general_statistics, name='general_statistics'),
]