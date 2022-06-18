from django.shortcuts import render
from rest_framework import viewsets, filters
from .serializers import VideoSerializer
from .models import Video

# Create your views here.


class VideoView(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by('-published_at')  # latest first
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description',)
