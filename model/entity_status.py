from abc import ABC, abstractmethod
from chapter import newChapter

class Status(ABC):
    @abstractmethod
    def String(self) -> str:
        pass

class StatusLinkBroken(Status):
    def String(self) -> str:
        return "Link broken"

class StatusUpToDate(Status):
    def String(self) -> str:
        return "Up to date"

class StatusNewChapterAvailable(Status):
    def __init__(self, remainingChapter: int):
        self.RemainingChapter = remainingChapter

    def String(self) -> str:
        return str(self.RemainingChapter) + " new chapter available"

def NewStatus(url: str, chapter: any) -> Status:
    nbChapter, err = newChapter(url, chapter)
    if err != None:
        return StatusLinkBroken()

    if nbChapter == 0:
        return StatusUpToDate()

    return StatusNewChapterAvailable(nbChapter)