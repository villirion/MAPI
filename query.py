import requests
from bs4 import BeautifulSoup
from handle_site import getSite
from error import Error, ErrorInvalidPayload

def pageExist(url: str) -> bool:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        return response.status_code // 100 == 2
    except requests.RequestException:
        return False

def isValid(url: str, chapter: str) -> bool:
    if not pageExist(url):
        return False

    chapterFound = chapterExist(url, str(chapter))

    return chapterFound

def getStatus(url: str, chapter: int) -> tuple[str]:
    nbChapter, err = newChapter(url, chapter)
    if err != None:
        return "Link broken"

    if nbChapter == 0:
        return "Up to date"

    return str(nbChapter) + " new chapter available"

def newChapter(url: str, chapter: int) -> tuple[int, Error]:
    if not pageExist(url):
        return 0, ErrorInvalidPayload()

    i = 1
    chapterFound = chapterExist(url, str(chapter + i))
    while chapterFound:
        i += 1
        chapterFound = chapterExist(url, str(chapter + i))

    return (i - 1), None

def chapterExist(url: str, chapter: str) -> bool:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
    except requests.RequestException:
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    site, err = getSite(url)
    if err != None:
        return False

    return site.chapterExist(soup, chapter)