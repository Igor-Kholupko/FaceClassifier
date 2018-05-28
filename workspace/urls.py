from django.urls import path
from django.conf.urls import url
from workspace import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('statistics/', views.statistics, name='user_statistics'),
    path('general_statistics/', views.general_statistics, name='log_general_statistics'),
    url(r'^user_statistics/(?P<pk>\d+)/$', views.statistics_detail, name='log_statistics_detail'),
]
