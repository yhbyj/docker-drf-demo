# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/29 10:13'

from django.urls import path

from user.views import CreateUserView, AuthTokenView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', AuthTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
