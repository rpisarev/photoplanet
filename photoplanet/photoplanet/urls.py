from django.conf.urls import patterns, include, url
#from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import HomePhotoListView, AllPhotoListView, PhotoDetailView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', HomePhotoListView.as_view(), name='home'),
    url(
        r'^load_photos/$', 'photoplanet.views.load_photos',
        name='load_photos'
    ),
    url(r'^all/$', AllPhotoListView.as_view(), name='all'),
    url(
        r'^photo/(?P<pk>\w+)$',
        PhotoDetailView.as_view(),
        name='photo-detail'
    ),
    url(r'^feedback/', include('feedback.urls')),
    url(r'', include('social_auth.urls')),
    url(r'', include('users.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '/'
        }, name='logout'),
    url(r'^input/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
