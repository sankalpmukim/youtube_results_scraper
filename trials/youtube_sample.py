# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from dotenv import load_dotenv
import googleapiclient.discovery
import googleapiclient.errors

load_dotenv()

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=os.getenv("YOUTUBE_API_KEY"), )

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q="surfing"
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
