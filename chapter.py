from bs4 import BeautifulSoup
from model.entity_site import getSite
from model.entity_error import Error, ErrorInvalidPayload
from query import pageExist


def newChapter(url: str, chapter: any) -> tuple[int, Error]:
    if not isinstance(chapter, int):
        chapter = int(chapter)

    response, ok = pageExist(url)
    if not ok:
        return 0, ErrorInvalidPayload()

    site, err = getSite(url)
    if err is not None:
        return 0, ErrorInvalidPayload()

    soup = BeautifulSoup(response.text, 'html.parser')

    i = 1
    while site.chapterExist(soup, str(chapter + i)):
        i += 1

    nbChapter = i - 1

    return nbChapter, None


def chapterExist(url: str, chapter: str) -> bool:
    response, ok = pageExist(url)
    if not ok:
        return False

    site, err = getSite(url)
    if err is not None:
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    return site.chapterExist(soup, chapter)
