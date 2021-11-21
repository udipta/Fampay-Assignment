""" This module contains services that get results from youtube and add in the database"""

from datetime import datetime
from threading import Thread
import time
from googleapiclient import discovery
from django.db import connections
from django.utils import timezone

from .models import *


def youtube_search_keyword(query: str = 'food', max_results: int = 10):
    """Fetching the latest videos for a search query using Youtube Data API.

    Args:
        query (str): search query.
        max_results(int): Maximum no of results we want in response from the Y
            Youtube Data API.

    Returns:
        results (list): List of all the videos data in dict format.
    """
    api_keys = APIKey.objects.filter(is_limit_over=False)
    results = list()

    if not len(api_keys):
        return results
    try:
        # Creating youtubeAPI object with the apikey
        youtube_object = discovery.build(serviceName="youtube", version="v3", developerKey=api_keys[0])
        results = youtube_object.search().list(q=query, part="id, snippet", maxResults=max_results).execute().get("items", [])
    except Exception as e:
        api_keys[0].is_limit_over = True
        api_keys[0].save()
        print("APIKey's Quota is over")
    finally:
        return results


def get_datetime_object(datetime_str):
    """Create a datetime object from string of date and time.

    Args:
        datetime_str (str): String contains date and time.

    Return:
        obj: Returns a datetime object.
    """
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.get_current_timezone())


def get_desired_video_dict_from_result(result):
    """ Extract relevant values from Youtube Data API Results for video.

    Args:
        result (dict): Youtube Data API result in dictionary format.

    Returns:
        dict: Returns relevant values of result for video.
    """

    return {
        'title': result["snippet"].get('title', ''),
        'description': result['snippet'].get('description', ''),
        'video_id': result['id'].get('videoId', ''),
        'channel_id': result['snippet'].get('channelId', ''),
        'published': get_datetime_object(result['snippet']['publishedAt']),
    }


def get_video_thumbnails_from_result(result):
    """ Extract relevant values from Youtube Data API Results
    for video thumbnails.

    Args:
        result (dict): Youtube Data API result in dictionary format.

    Returns:
        list: Returns relevant values of result for video thumbnails.
    """
    return [{
        'screen_size': screen_size,
        'url': result['snippet']['thumbnails'][screen_size]['url'],
    } for screen_size in result['snippet']['thumbnails']]


def save_video_and_thumbnail_in_models(result):
    """Save video and it's thumbnails in Database.

    Args:
        result (dict): Youtube Data API result in dictionary format.
    """

    video_dict = get_desired_video_dict_from_result(result)
    video_obj = Video(**video_dict)
    video_obj.save()

    thumbnails = get_video_thumbnails_from_result(result)
    for thumbnail in thumbnails:
        thumbnail['video'] = video_obj
        thumbnail_obj = VideoThumbNail(**thumbnail)
        thumbnail_obj.save()

    # Closing all connections before delay to overcome concurrency
    for conn in connections.all():
        conn.close()


def get_time_of_most_recent_uploaded_video():
    """Returns time of most recent uploaded video.

    Returns:
        resent_publish_datetime (datetime): Returns datetime object.
    """

    resent_publish_datetime = timezone.now()
    search_results = youtube_search_keyword()

    for result in search_results:
        publish_datetime = get_datetime_object(result['snippet']['publishedAt'])
        save_video_and_thumbnail_in_models(result)
        resent_publish_datetime = max(resent_publish_datetime, publish_datetime)
    return resent_publish_datetime


def search_and_add_youtube_videos_service():
    """function for fetching the latest videos
    for a search query and should storing it in database.
    """
    resent_publish_datetime = get_time_of_most_recent_uploaded_video()

    while True:
        search_results = youtube_search_keyword()
        for result in search_results:
            video_publish_datetime = get_datetime_object(result['snippet']['publishedAt'])
            if resent_publish_datetime < video_publish_datetime:
                save_video_and_thumbnail_in_models(result)
                resent_publish_datetime = video_publish_datetime
        time.sleep(10*60)


def start_searching_and_adding_youtube_videos():
    """Start services for searching and adding youtube videos."""
    while True:
        if APIKey.objects.filter(is_limit_over=False).exists():
            Thread(target=search_and_add_youtube_videos_service).start()
        time.sleep(10*60)


service_thread = Thread(target=start_searching_and_adding_youtube_videos)
