from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('general_statistics/', views.general_statistics, name='unlog_general_statistics'),
    url(r'^user_statistics/(?P<pk>\d+)/$', views.statistics_detail, name='unlog_statistics_detail'),
]
