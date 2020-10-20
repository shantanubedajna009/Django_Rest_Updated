from django.conf.urls import url
from django.views.generic import RedirectView

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import CustomAuthAPIView, RegisterAPIView


app_name = 'accounts_api'

urlpatterns = [
    url(r'^$', CustomAuthAPIView.as_view()),
    url(r'^register/$', RegisterAPIView.as_view(), name='register'),
    url(r'^jwt/$', obtain_jwt_token, name='auth_token'),
    url(r'^jwt/refresh/$', refresh_jwt_token, name='auth_token_refresh'),

]