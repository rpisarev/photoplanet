from django.conf.urls import patterns, url
from feedback.views import FBackView


urlpatterns = patterns(
    '',
    url(r'^$', FBackView.as_view(), name='feedback'),
)
