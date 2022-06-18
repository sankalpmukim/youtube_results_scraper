from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'published_at',
                    'thumbnail', 'duration')

# Register your models here.


admin.site.register(Video, VideoAdmin)
