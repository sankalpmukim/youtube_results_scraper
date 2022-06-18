from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'published_at',
                    'url', 'thumbnail',)
    list_filter = ('published_at', )
    list_per_page = 25
    ordering = ('-published_at',)  # latest first
    search_fields = ('title', 'description',)

# Register your models here.


admin.site.register(Video, VideoAdmin)
