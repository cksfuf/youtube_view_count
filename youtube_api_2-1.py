import requests
from pprint import pprint
import pandas as pd
import os
from dotenv import load_dotenvs

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')

SEARCH_URL = 'https://youtube.googleapis.com/youtube/v3/search'
VIDEOS_URL = 'https://youtube.googleapis.com/youtube/v3/videos'

# programs = ['오은영의 금쪽 상담소', '아빠는 꽃중년', '남의 나라 살아보기 선 넘은 패밀리', '채널A 토일드라마 새벽 2시의 신데렐라', '요즘 남자 라이프 신랑수업', '요즘 육아 금쪽같은 내 새끼', '탐정들의 영업비밀', '절친 토크멘터리 4인용 식탁', '성적을 부탁해 티쳐스', '이제 만나러 갑니다']
youtube_id_list = []

params = {
    'part': 'snippet',
    'maxResults': 50,
    'q': '요즘 육아 금쪽같은 내 새끼',
    'key': api_key,
}


while len(youtube_id_list) < 200:
    res = requests.get(SEARCH_URL, params=params)
    result = res.json()


    for item in result.get('items'):
        youtube_id = item.get('id').get('videoId')
        if youtube_id:
            youtube_id_list.append(youtube_id)
            if len(youtube_id_list) >= 200:
                break

    if 'nextPageToken' in result and len(youtube_id_list) < 200:
        params['pageToken'] = result['nextPageToken']
    else:
        break

    if len(youtube_id_list) >= 200:
        break



video_result = {
    'title': [],
    'view_count': [],
    'like_count': [],
    'channel_name': [],
    'published': []
}

for youtube_id in youtube_id_list:
    params = {
        'part': 'statistics, snippet',
        'id': youtube_id,
        'key': api_key,
    }

    res = requests.get(VIDEOS_URL, params=params)
    result = res.json()

    title = result.get('items')[0].get('snippet').get('title')
    view_count = result.get('items')[0].get('statistics').get('viewCount')
    like_count = result.get('items')[0].get('statistics').get('likeCount')
    channel_name = result.get('items')[0].get('snippet').get('channelTitle')
    published = result.get('items')[0].get('snippet').get('publishedAt')

    video_result['title'].append(title)
    video_result['view_count'].append(view_count)
    video_result['like_count'].append(like_count)
    video_result['channel_name'].append(channel_name)
    video_result['published'].append(published)


df = pd.DataFrame(video_result)
df.to_csv('요즘 육아 금쪽같은 내 새끼.csv', index=False)