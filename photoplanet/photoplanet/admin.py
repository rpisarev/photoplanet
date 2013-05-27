from django.contrib import admin
from .models import Photo, Vote


class PhotoAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Photo, PhotoAdmin)
dmin.site.register(Vote)
