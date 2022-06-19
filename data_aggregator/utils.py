from .models import ApiKey
import os


def set_api_keys():
    """
    Set API keys from environment variables to the database.
    """
    if ApiKey.objects.all().count() == 0:
        count = int(os.getenv("YOUTUBE_API_KEY_COUNT"))
        for i in range(1, count+1):
            key = os.getenv(f"YOUTUBE_API_KEY_{i}")
            obj = ApiKey(api_key=key)
            obj.save()
