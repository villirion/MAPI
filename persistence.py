import pandas as pd
from query import getStatus
from datetime import datetime
from error import Error

def GetAll(df: pd.DataFrame) -> list[dict]:
    jsonList = []

    for _, row in df.iterrows():
        rowDict = row.to_dict()
        jsonList.append(rowDict)

    jsonList_sorted = sorted(jsonList, key=lambda x: x['CHAPTER'], reverse=True)

    return jsonList_sorted

def Exist(df: pd.DataFrame, title: str) -> bool:
    df_copy = df.copy()
    entryExist = df_copy[df_copy["TITLE"] == title]

    if entryExist.empty:
        return False

    return True

def Insert(df: pd.DataFrame, title: str, url: str, chapter: any, status: str, date: any) -> Error:
    df.loc[len(df.index)] = [title, url, chapter, status, date]

    return None

def Replace(df: pd.DataFrame, title: str, url: str, chapter: any, status: str, date: any) -> Error:
    df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

    return None

def ReloadAll(df: pd.DataFrame):
    for _, row in df.iterrows():
        title = row['TITLE']
        url = row['SITE']
        chapter = row['CHAPTER']
        status = getStatus(url, chapter)
        date = datetime.now().date()
        df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

def Remove(df: pd.DataFrame, title: str) -> tuple[pd.DataFrame, Error]:
    df = df.drop(df.index[df["TITLE"] == title])

    return df, None