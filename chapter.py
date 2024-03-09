from bs4 import BeautifulSoup
from model.entity_site import getSite
from model.entity_error import Error, ErrorInvalidPayload
from query import pageExist

def checkDecimal(url: str, chapter: any) -> int:
    increment = 0.1
    current_chapter = chapter

    while chapterExist(url, str(current_chapter)):
        current_chapter += increment

    return increment * 10 - 1

def newChapter(url: str, chapter: any) -> tuple[int, Error]:
    _, ok = pageExist(url)
    if not ok:
        return 0, ErrorInvalidPayload()

    i = 1
    if chapter % 1 != 0:
        nbChapter = checkDecimal(url, chapter)

        new_chapter = int(chapter) + 1

        if not chapterExist(url, str(new_chapter)):
            new_chapter += 0.1

            if not chapterExist(url, str(new_chapter)):
                return 0, None

            new_chapter -= 0.1

        nbChapter += 1

        while i != 0:
            i = checkDecimal(url, new_chapter)
            nbChapter += i
            new_chapter += 1

        return int(nbChapter), None

    chapter = int(chapter)
    current_chapter = chapter

    while chapterExist(url, str(current_chapter + i)):
        i += 1

    nbChapter = i - 1

    return nbChapter, None

def chapterExist(url: str, chapter: str) -> bool:
    response, ok = pageExist(url)
    if not ok:
        return False

    site, err = getSite(url)
    if err != None:
        return False

    soup = BeautifulSoup(response.text, 'html.parser')

    return site.chapterExist(soup, chapter)