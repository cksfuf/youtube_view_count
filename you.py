#  pip install webdriver_manager selenium openpyxl pytube pandas lxml beautifulsoup4
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import lxml
import requests
import re

# program = ('오은영의 금쪽 상담소', '아빠는 꽃중년', '남의 나라 살아보기 선 넘은 패밀리', '채널A 토일드라마 새벽 2시의 신데렐라', '요즘 남자 라이프 신랑수업', '요즘 육아 금쪽같은 내 새끼', '탐정들의 영업비밀', '절친 토크멘터리 4인용 식탁')
programs = ['요즘 남자 라이프 신랑수업', '요즘 육아 금쪽같은 내 새끼', '탐정들의 영업비밀', '절친 토크멘터리 4인용 식탁']
for program in programs:
    driver = wb.Chrome() 
    url = f"https://www.youtube.com/results?search_query={program}"
    driver.get(url)

    video_btn_selector = "yt-formatted-string[title='동영상']"
    button = driver.find_element(By.CSS_SELECTOR, video_btn_selector)

    button.click()


    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    for i in range(1,10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)


    soup = bs(driver.page_source, 'html.parser')

    title =soup.select('a#video-title')

    # 조회수와 날짜
    view = soup.select('span.style-scope.ytd-video-meta-block')

    title_list = []
    view_list = []
    time_list = []

    for i in range(len(title)):
        title_list.append(title[i].text.strip())
        view_list.append(view[2*i].text.strip())
        time_list.append(view[2*i+1].text.strip())


    info = {
        '제목': title_list,
        '조회수': view_list,
        '업로드': time_list
    }
    results_df = pd.DataFrame(info)
    results_df.to_csv(f'{program}.csv', index=False)
print(pd.DataFrame(info))