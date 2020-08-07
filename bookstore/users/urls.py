from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^register_handler/', views.register_handler, name='register_handler'),
    url(r'^login/', views.login, name='login'),
    url(r'^login_check/', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'), # 退出用户登录
    url(r'', views.user, name='user'),

]
