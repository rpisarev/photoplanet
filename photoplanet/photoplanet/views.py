from django.http import HttpResponse
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.dates import DayArchiveView
from annoying.decorators import ajax_request
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from datetime import date
from braces.views import LoginRequiredMixin

from .models import Photo, Vote

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
        order_by('-vote_count', '-like_count').all()
    context_object_name = 'photo_list'
    paginate_by = 10


class AllPhotoListView(ListView):
    model = Photo
    template_name = 'photoplanet/all.html'
    context_object_name = 'photo_list'
    paginate_by = 10
    queryset = Photo.objects.order_by('-created_time').all()


class VotePhotosListView(LoginRequiredMixin, AllPhotoListView):
    """
    AllPhotoListView -> VotePhotosListView (AllPhotoListView parent)
    """
    def get_queryset(self):
        return Photo.objects.exclude(
            photo_id__in=Vote.objects.filter(
                user_id=self.request.user.id).values_list('photo_id', flat=True)
        ).order_by('-created_time')


class PhotoDetailView(DetailView):
    model = Photo


class PhotoPerDayArchiveView(DayArchiveView):
    model = Photo
    template_name = 'photoplanet/photo_day.html'
    queryset = Photo.objects.order_by('-vote_count', '-like_count').all()
    date_field = "created_time"
    month_format = '%m'
    make_object_list = True
    allow_empty = True
    paginate_by = 10


class AboutListView(ListView):
    template_name = 'photoplanet/about.html'
    model = Photo


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


@require_POST
@ajax_request
@csrf_protect
def vote(request):
    """View for AJAX voting"""
    user = request.user
    photo_id = request.POST['photo']
    photo = Photo.objects.get(photo_id=photo_id)
    if user.is_authenticated():
        vote_type = request.POST['vote']
        if '-1' in vote_type:
            vote_value = -1
        elif '+1' in vote_type:
            vote_value = 1
        elif '1' in vote_type:
            vote_value = 1
        else:
            vote_value = 0
        vote_obj = Vote(user=user, photo=photo, rating=vote_value)
        vote_obj.save()
        photo = Photo.objects.get(photo_id=photo_id)
        context_dict = {
            'votes': photo.vote_count,
            'message': 'Vote is updated.',
        }

    else:
        context_dict = {
            'message': 'You must be logged in to vote.',
        }
    return context_dict
