from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('general_statistics/', views.general_statistics, name='unlog_general_statistics'),
]
