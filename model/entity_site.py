import re
from abc import ABC, abstractmethod
from model.entity_error import Error, ErrorInvalidPayload
from bs4 import BeautifulSoup, Comment
from query import pageExist
from title import toPersistedTitle

class Site(ABC):
    @abstractmethod
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pass

    def reloadURL(self, title: str) -> str:
        pass

class Asuratoon(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(^{chapter})(.*)')
        chapterFound = soup.find('li', {'data-num': pattern})

        if not chapterFound:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        response, ok = pageExist("https://asuratoon.com/?s=" + title)
        if not ok:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        urlFound = soup.find('a', {'title': toPersistedTitle(title)})
        if not urlFound:
            return None

        return urlFound.get('href')


class Lumitoon(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        chapterFound = soup.find('li', {'data-num': chapter})

        if not chapterFound:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        response, ok = pageExist("https://lumitoon.com/?s=" + title)
        if not ok:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        urlFound = soup.find('a', {'title': toPersistedTitle(title)})
        if not urlFound:
            return None

        return urlFound.get('href')

class Manga4life(Site):
    def __init__(self, url: str):
        self.url = url

    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        name = self.url.split("/")[-1]
        chapterURL = "https://manga4life.com/read-online/" + name + "-chapter-" + chapter + ".html"
        response, ok = pageExist(chapterURL)
        if not ok:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        wrongResponse = soup.find(string=lambda text: isinstance(text, Comment) and '404' in text)
        if wrongResponse:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        return None

class Flamecomics(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        chapterFound = soup.find('li', {'data-num': chapter})

        if not chapterFound:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        response, ok = pageExist("https://flamecomics.com/?s=" + title)
        if not ok:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        urlFound = soup.find('a', {'title': toPersistedTitle(title)})
        if not urlFound:
            return None

        return urlFound.get('href')

class Mangaclash(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(.*)({chapter}/)$')
        chapterFound = soup.find('a', href=pattern)

        if not chapterFound:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        return None

class Reaperscans(Site):
    def chapterExist(self, soup: BeautifulSoup, chapter: str) -> bool:
        pattern = re.compile(fr'(.*)(-chapter-{chapter})$')
        chapterFound = soup.find('a', href=pattern)

        if not chapterFound:
            return False

        return True

    def reloadURL(self, title: str) -> str:
        return None

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