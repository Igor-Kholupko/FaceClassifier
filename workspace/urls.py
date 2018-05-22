from django.urls import path
from workspace import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('statistics/', views.statistics, name='user_statistics'),
    path('general_statistics/', views.general_statistics, name='log_general_statistics'),
]
