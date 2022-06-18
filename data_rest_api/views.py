from django.shortcuts import render
from rest_framework import viewsets
from .serializers import VideoSerializer
from .models import Video

# Create your views here.


class VideoView(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by('-published_at')
