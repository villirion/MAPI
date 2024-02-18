import requests
from persistence import setupCSV
from bs4 import BeautifulSoup
import re
import time

def check_page_existence(url: str) -> bool:
    try:
        response = requests.head(url)
        return response.status_code // 100 == 2
    except requests.RequestException:
        return False

def check_all_page_existence(csv: str) -> list[dict]:
    df = setupCSV(csv)

    json_list = []

    for _, row in df.iterrows():
        if not check_page_existence(row['SITE']):
            row_dict = row.to_dict()
            json_list.append(row_dict)

    return json_list

def check_all_new_chapter(csv: str) -> list[dict]:
    df = setupCSV(csv)

    json_list = []

    for _, row in df.iterrows():
        chapter = int(row['CHAPTER']) + 1
        if check_page_existence(get_last_chapter_url(row['SITE'], str(chapter))):
            row_dict = row.to_dict()
            json_list.append(row_dict)

    return json_list

def get_last_chapter_url(url: str, chapter: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if "lumitoon.com" in url or "flamecomics.com" in url:
        chapter_li = soup.find('li', {'data-num': chapter})

        if chapter_li:
            chapter_url = chapter_li.find('a')['href']
            return chapter_url

    elif "asuratoon.com" in url:
        pattern = re.compile(fr'(^{chapter})(.*)')
        chapter_li = soup.find('li', {'data-num': pattern})

        if chapter_li:
            chapter_url = chapter_li.find('a')['href']
            return chapter_url

    elif "manga4life.com" in url:
        pattern = re.compile(fr'(.*)({chapter}.html)$')
        chapter_a = soup.find('a', href= pattern)

        if chapter_a:
            chapter_url = chapter_a.get('href')
            return chapter_url

    elif "mangaclash.com" in url:
        pattern = re.compile(fr'(.*)({chapter}/)$')
        chapter_a = soup.find('a', href= pattern)

        if chapter_a:
            chapter_url = chapter_a.get('href')
            return chapter_url

    elif "reaperscans.com" in url:
        pattern = re.compile(fr'(.*)(-chapter-{chapter})$')
        chapter_li = soup.find('a', href=pattern)

        if chapter_li:
            chapter_url = chapter_li.get('href')
            return chapter_url
