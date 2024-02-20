from abc import ABC, abstractmethod
from error import Error, ErrorInvalidPayload, ErrorNotFound
import re
from bs4 import BeautifulSoup, Comment
import requests

class Site(ABC):
    @abstractmethod
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pass

class Asuratoon(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(^{chapter})(.*)')
        chapterFound = soup.find('li', {'data-num': pattern})

        if chapterFound:
            #chapterURL = chapterFound.find('a')['href']
            return True

        return False

class Lumitoon(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        chapterFound = soup.find('li', {'data-num': chapter})

        if chapterFound:
            #chapterURL = chapterFound.find('a')['href']
            return True

        return False

class Manga4life(Site):
    def __init__(self, url: str):
        self.url = url

    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        name = self.url.split("/")[-1]
        chapterURL = "https://manga4life.com/read-online/" + name + "-chapter-" + chapter + ".html"
        try:
            response = requests.get(chapterURL, headers=headers)
        except requests.RequestException:
            return False

        if response.status_code // 100 == 2:
            soup = BeautifulSoup(response.text, 'html.parser')

            error = '404'
            chapterFoundError = soup.find(string=lambda text: isinstance(text, Comment) and error in text)
            if not chapterFoundError:
                return True

        return False

class Flamecomics(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        chapterFound = soup.find('li', {'data-num': chapter})

        if chapterFound:
            #chapterURL = chapterFound.find('a')['href']
            return True

        return False

class Mangaclash(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(.*)({chapter}/)$')
        chapterFound = soup.find('a', href=pattern)

        if chapterFound:
            #chapterURL = chapterFound.get('href')
            return True

        return False

class Reaperscans(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(.*)(-chapter-{chapter})$')
        chapterFound = soup.find('a', href=pattern)

        if chapterFound:
            #chapterURL = chapterFound.get('href')
            return True

        return False

def getSite(url: str) -> tuple[Site, Error]:
    if "lumitoon.com" in url:
        return Lumitoon(), None

    if "asuratoon.com" in url:
        return Asuratoon(), None

    if "manga4life.com" in url:
        return Manga4life(url), None

    if "mangaclash.com" in url:
        return Mangaclash(), None

    if "flamecomics.com" in url:
        return Flamecomics(), None

    if "reaperscans.com" in url:
        return Reaperscans(), None

    return None, ErrorInvalidPayload()