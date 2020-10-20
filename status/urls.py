from django.conf.urls import url
from django.views.generic import RedirectView


app_name = 'status'


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/')),
]