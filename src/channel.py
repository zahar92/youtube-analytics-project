import json
import os
from googleapiclient.discovery import build
from helper.youtube_api_manual import printj


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.channel['items'][0]['id']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет информацию о канале в формате json"""
        data = {
            'ID Chanel': self.channel_id,
            'Name': self.title,
            'Description': self.description,
            'URL': self.url,
            'Count of subscribers': self.subscriber_count,
            'Count of videos': self.video_count,
            'Count of views': self.view_count,
        }
        with open(file_name, 'w', encoding='utf-8') as outfile:
            outfile.write(json.dumps(data, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
