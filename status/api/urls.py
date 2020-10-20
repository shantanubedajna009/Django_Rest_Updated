from django.conf.urls import url

from .views import (
    StatusListAPIView,
    # StatusCreateAPIView,
    StatusDetailAPIView,
    # StatusUpdateAPIView,
    # StatusDeleteAPIView,
    )

app_name = 'status_api'

urlpatterns = [
    url(r'^$', StatusListAPIView.as_view(), name='list'),
    # url(r'^create/$', StatusCreateAPIView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$', StatusDetailAPIView.as_view(), name='detail'), # the IsOwnerOrReadOnly applied in this endpoint
    # url(r'^(?P<id>\d+)/update/$', StatusUpdateAPIView.as_view(), name='update'),
    # url(r'^(?P<id>\d+)/delete/$', StatusDeleteAPIView.as_view(), name='delete'),
    
]