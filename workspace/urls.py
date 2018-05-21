from django.urls import path
from workspace import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('statistics/', views.statistics, name='statistics'),
]


