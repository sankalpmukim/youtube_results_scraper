from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'url',
                    'published_at', 'thumbnail',)

# Register your models here.


admin.site.register(Video, VideoAdmin)
