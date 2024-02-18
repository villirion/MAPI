import requests
from bs4 import BeautifulSoup, Comment
import re

def check_page_existence(url: str) -> bool:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        return response.status_code // 100 == 2
    except requests.RequestException:
        return False

def check_valid(url: str, chapter: str) -> str:
    if not check_page_existence(url):
        return False

    chapter_url = get_chapter_url(url, str(chapter))
    if chapter_url == "" or chapter_url == "Unsupported site":
        return False

    return True

def get_status(url: str, chapter: int) -> str:
    if not check_page_existence(url):
        return "Link broken"

    chapter_url = get_chapter_url(url, str(chapter + 1))
    if chapter_url == "Unsupported site":
        return "Unsupported site"

    if chapter_url != "":
        return "New chapter available"

    return "Up to date"

def get_chapter_url(url: str, chapter: str) -> str:
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
        name = url.split("/")[-1]
        chapter_url = "https://manga4life.com/read-online/" + name + "-chapter-" + chapter + ".html"

        if check_page_existence(chapter_url):
            response = requests.get(chapter_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            comment_text = '404'
            find = soup.find(string=lambda text: isinstance(text, Comment) and comment_text in text)
            if not find:
                return chapter_url

    elif "mangaclash.com" in url:
        pattern = re.compile(fr'(.*)({chapter}/)$')
        chapter_a = soup.find('a', href=pattern)

        if chapter_a:
            chapter_url = chapter_a.get('href')
            return chapter_url

    elif "reaperscans.com" in url:
        pattern = re.compile(fr'(.*)(-chapter-{chapter})$')
        chapter_li = soup.find('a', href=pattern)

        if chapter_li:
            chapter_url = chapter_li.get('href')
            return chapter_url

    else:
        return "Unsupported site"

    return ""