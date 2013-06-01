from django.contrib import admin
from .models import Photo, Vote


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'photo_id',
        'username',
        'user_avatar_url',
        'photo_url',
        'created_time',
        'like_count',
        'vote_count',
        'is_spam'
    )
    readonly_fields = ['created_time', 'like_count',]
    search_fields = ['name']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Vote)
