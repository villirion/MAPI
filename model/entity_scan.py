
from model.entity_error import Error, ErrorInvalidPayload
from chapter import chapterExist
from model.entity_status import NewStatus, Status

class Scan():
    def __init__(self, title: str, url: str, chapter: any):
        self.url = url
        self.chapter = chapter
        self.title = title
        status = NewStatus(url, chapter)
        self.status = status.String()

    def URL(self) -> str:
        return self.url

    def Chapter(self) -> any:
        return self.chapter

    def Title(self) -> str:
        return self.title

    def Status(self) -> Status:
        return self.status

def NewScan(title: str, url: str, chapter: any) -> tuple[Scan, Error]:
    if not isValid(url, chapter):
        return None, ErrorInvalidPayload()

    return Scan(title, url, chapter), None

def InstatiateScanFromDataframe(title: str, url: str, chapter: any) -> Scan:
    return Scan(title, url, chapter)


def isValid(url: str, chapter: any) -> bool:
    return chapterExist(url, str(chapter))