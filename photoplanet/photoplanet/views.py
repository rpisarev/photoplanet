from django.http import HttpResponse
from django.conf import settings
from django.views.generic import ListView

from datetime import date
from .models import Photo

from instagram.client import InstagramAPI


LARGE_MEDIA_MAX_ID = 100000000000000000
MEDIA_COUNT = 20
MEDIA_TAG = 'donetsk'
PHOTOS_PER_PAGE = 10


class HomePhotoListView(ListView):
    model = Photo
    template_name = 'photoplanet/all.html'
    queryset = Photo.objects.filter(
        created_time__gte=date.today()).\
        order_by('-like_count')
    context_object_name = 'photo_list'
    paginate_by = 10


class AllPhotoListView(ListView):
    model = Photo
    template_name = 'photoplanet/all.html'
    context_object_name = 'photo_list'
    paginate_by = 10
    queryset = Photo.objects.order_by('-created_time').all()


def load_photos(request):
    """
    Loads photos from Insagram (not yet other,like G+) and insert in database.
    """

    api = InstagramAPI(
        client_id=settings.INSTAGRAM_CLIENT_ID,
        client_secret=settings.INSTAGRAM_CLIENT_SECRET)
    search_result = api.tag_recent_media(
        MEDIA_COUNT, LARGE_MEDIA_MAX_ID, MEDIA_TAG
    )
    info_photo = ''

    for m in search_result[0]:
        photo, is_created = Photo.objects.get_or_create(
            photo_id=m.id, username=m.user.username)
        is_like_count_updated = False
        if not photo.like_count == m.like_count:
            photo.username = m.user.username
            photo.user_avatar_url = m.user.profile_picture
            photo.photo_url = m.images['standard_resolution'].url
            photo.created_time = m.created_time
            photo.like_count = m.like_count
            photo.save()
            is_like_count_updated = True
        info_photo += '<li>{} {} {} {} {} {} {} {}</li>'.format(
            m.id,
            m.user.username,
            '<img src="{}"/>'.format(m.user.profile_picture),
            '<img src="{}"/>'.format(m.images['standard_resolution'].url),
            m.created_time,
            m.like_count,
            is_created,
            is_like_count_updated
        )

    html = "<html><body><ul>{}</ul></body></html>".format(info_photo)
    return HttpResponse(html)
