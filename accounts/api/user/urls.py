from django.conf.urls import url
from .views import UserDetailApiView, UserStatusListView

app_name = 'api-user'

urlpatterns = [
    url(r'^(?P<username>\w+)/$', UserDetailApiView.as_view(), name='detail'),
    url(r'^(?P<username>\w+)/status/$', UserStatusListView.as_view(), name='status-list'),
]