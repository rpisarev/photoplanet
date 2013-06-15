# https://docs.djangoproject.com/en/1.5/howto/custom-management-commands/
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import utc

from instagram.client import InstagramAPI

from photoplanet.models import Photo


# TODO: refactor! this is duplicated in views.py
LARGE_MEDIA_MAX_ID = 100000000000000000
MEDIA_COUNT = 100
MEDIA_TAG = 'donetsk'


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = 'Loads recent photos'

    def handle(self, *args, **options):
        # raise CommandError('Some error.')
        api = InstagramAPI(
            client_id=settings.INSTAGRAM_CLIENT_ID,
            client_secret=settings.INSTAGRAM_CLIENT_SECRET)
        search_result = api.tag_recent_media(
            MEDIA_COUNT, LARGE_MEDIA_MAX_ID, MEDIA_TAG
        )
        info = ''
        # list of media is in the first element of the tuple
        for m in search_result[0]:
            photo, is_created = Photo.objects.get_or_create(
                photo_id=m.id, username=m.user.username)
            is_like_count_updated = False
            if not photo.like_count == m.like_count:
                photo.username = m.user.username
                photo.user_avatar_url = m.user.profile_picture
                photo.photo_url = m.images['standard_resolution'].url
                photo.created_time = m.created_time.replace(tzinfo=utc)
                photo.like_count = m.like_count
                photo.save()
                is_like_count_updated = True
            info = ''
            info += '{id}\n{username}\n{avatar_url}\n{photo_url}\n'.format(
                id=m.id,
                username=m.user.username,
                avatar_url=m.user.profile_picture,
                photo_url=m.images['standard_resolution'].url
            )
            info += '{created}\n{like}\n{is_created}\n{is_updated}\n'.format(
                created=m.created_time,
                like=m.like_count,
                is_created=is_created,
                is_updated=is_like_count_updated
            )
            info += 40 * '-'
            self.stdout.write(info)
