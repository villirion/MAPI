import pandas as pd
from query import getStatus, isValid
from datetime import datetime
from error import Error, ErrorInvalidPayload, ErrorNotFound, ErrorInvalidFormat

def setupCSV(csv: str) -> pd.DataFrame:
    df = pd.read_csv(csv)

    return df

def updateCSV(df: pd.DataFrame, csv: str) -> pd.DataFrame:
    df.to_csv(csv, index=False)

def List(csv: str) -> list[dict]:
    df = setupCSV(csv)

    jsonList = []

    for _, row in df.iterrows():
        rowDict = row.to_dict()
        jsonList.append(rowDict)

    return jsonList

"""
def Get(csv: str, title: str) -> tuple[dict, Error]:
    df = setupCSV(csv)

    entryExist = df[df["TITLE"] == title]

    if entryExist.empty:
        return None, ErrorNotFound()

    row = entryExist.iloc[0]
    jsonRow = row.to_dict()

    return jsonRow, None
"""

def Post(csv: str, data: dict) -> Error:
    df = setupCSV(csv)

    requiredKeys = {'TITLE', 'SITE', 'CHAPTER'}
    if not requiredKeys.issubset(data.keys()):
        return ErrorInvalidFormat()

    title = data['TITLE']
    url = data['SITE']
    chapter = data['CHAPTER']

    if not isValid(url, chapter):
        return ErrorInvalidPayload()

    status = getStatus(url, chapter)
    date = datetime.now().date()

    df.loc[len(df.index)] = [title, url, chapter, status, date]

    updateCSV(df, csv)

    return None

def Update(csv: str, data: dict) -> Error:
    df = setupCSV(csv)
    df_copy = df.copy()

    requiredKeys = {'TITLE', 'SITE', 'CHAPTER'}
    if not requiredKeys.issubset(data.keys()):
        return ErrorInvalidFormat()

    title = data['TITLE']

    entryExist = df_copy[df_copy["TITLE"] == title]

    if entryExist.empty:
        return ErrorNotFound()

    url = data['SITE']
    chapter = data['CHAPTER']

    if not isValid(url, chapter):
        return ErrorInvalidPayload()

    status = getStatus(url, chapter)
    date = datetime.now().date()

    if entryExist.iloc[0]['CHAPTER'] == chapter and entryExist.iloc[0]['STATUS'] == status and entryExist.iloc[0]['SITE'] == url:
        return None

    df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

    updateCSV(df, csv)

    return None

def Reload(csv: str):
    df = setupCSV(csv)

    for _, row in df.iterrows():
        title = row['TITLE']
        url = row['SITE']
        chapter = row['CHAPTER']
        status = getStatus(url, chapter)
        date = datetime.now().date()
        df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

    updateCSV(df, csv)

def Delete(csv: str, data: dict) -> Error:
    df = setupCSV(csv)
    df_copy = df.copy()

    requiredKeys = {'TITLE'}
    if not requiredKeys.issubset(data.keys()):
        return ErrorInvalidFormat()

    title = data['TITLE']

    entryExist = df_copy[df_copy["TITLE"] == title]

    if entryExist.empty:
        return ErrorNotFound()

    df = df.drop(df.index[df["TITLE"] == title])

    updateCSV(df, csv)

    return None