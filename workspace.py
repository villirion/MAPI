import pandas as pd
from error import Error, ErrorInvalidPayload

manhwaCSV = "P:\\CSV\\manhwa.csv"
mangaCSV = "P:\\CSV\\manga.csv"

def setupCSV(csv: str) -> pd.DataFrame:
    df = pd.read_csv(csv)

    return df

def updateCSV(df: pd.DataFrame, csv: str) -> pd.DataFrame:
    df.to_csv(csv, index=False)

def getWorkspace(source: str) -> tuple[pd.DataFrame, Error]:
    if source == "manhwa":
        return setupCSV(manhwaCSV), None

    elif source == "manga":
        return setupCSV(mangaCSV), None

    return None, ErrorInvalidPayload

def saveWorkspace(df: pd.DataFrame, source: str) -> Error:
    if source == "manhwa":
        updateCSV(df, manhwaCSV)

        return None

    elif source == "manga":
        updateCSV(df, mangaCSV)

        return None

    return ErrorInvalidPayload