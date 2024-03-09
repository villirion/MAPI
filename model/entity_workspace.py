import pandas as pd
from model.entity_error import Error, ErrorInvalidPayload
from abc import ABC, abstractmethod

manhwaCSV = "P:\\CSV\\manhwa.csv"
mangaCSV = "P:\\CSV\\manga.csv"

class Workspace(ABC):
    @abstractmethod
    def DF(self) -> pd.DataFrame:
        pass

    def Save(self):
        pass

class MangaWorkspace(Workspace):
    def __init__(self):
        self.df = setupCSV(mangaCSV)

    def DF(self) -> dict:
        return self.df

    def Save(self):
        updateCSV(self.df, mangaCSV)

class ManhwaWorkspace(Workspace):
    def __init__(self):
        self.df = setupCSV(manhwaCSV)

    def DF(self) -> dict:
        return self.df

    def Save(self):
        updateCSV(self.df, manhwaCSV)

def setupCSV(csv: str) -> pd.DataFrame:
    df = pd.read_csv(csv)

    return df

def updateCSV(df: pd.DataFrame, csv: str) -> pd.DataFrame:
    df.to_csv(csv, index=False)

def getWorkspace(source: str) -> tuple[Workspace, Error]:
    if source == "manhwa":
        return ManhwaWorkspace(), None

    elif source == "manga":
        return MangaWorkspace(), None

    return None, ErrorInvalidPayload()