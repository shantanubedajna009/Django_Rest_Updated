from django.conf.urls import url, include
from .views import json_response

app_name = 'updates'

urlpatterns = [
    url(r'^json_func/$', json_response, name='json_func'),
]