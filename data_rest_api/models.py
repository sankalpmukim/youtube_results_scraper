from django.db import models

# Create your models here.


class Video(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail = models.URLField()

    def __str__(self) -> str:
        return self.title
