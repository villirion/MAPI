from query import getStatus, isValid
from datetime import datetime
from error import Error, ErrorInvalidPayload, ErrorInvalidFormat
from workspace import getWorkspace, saveWorkspace
from persistence import Insert, GetAll, Exist, Replace, ReloadAll, Remove

def List(source: str) -> list[dict]:
    df, err = getWorkspace(source)
    if err != None:
        return err

    return GetAll(df)

def Post(source: str, data: dict) -> Error:
    df, err = getWorkspace(source)
    if err != None:
        return err

    title, url, chapter, err = getKeys(data)
    if err != None:
        return err

    if not isValid(url, chapter):
        return ErrorInvalidPayload()

    status, date = getDateAndStatus(url, chapter)

    err = Insert(df, title, url, chapter, status, date)
    if err != None:
        return err

    err = saveWorkspace(df, source)
    if err != None:
        return err

    return None

def Update(source: str, data: dict) -> Error:
    df, err = getWorkspace(source)
    if err != None:
        return err

    title, url, chapter, err = getKeys(data)
    if err != None:
        return err

    if not Exist(df, title):
        return ErrorInvalidPayload()

    if not isValid(url, chapter):
        return ErrorInvalidPayload()

    status, date = getDateAndStatus(url, chapter)

    err = Replace(df, title, url, chapter, status, date)
    if err != None:
        return err

    err = saveWorkspace(df, source)
    if err != None:
        return err

    return None

def Delete(source: str, data: dict) -> Error:
    df, err = getWorkspace(source)
    if err != None:
        return err

    title, err = getKey(data)
    if err != None:
        return err

    if not Exist(df, title):
        return ErrorInvalidPayload()

    df, err = Remove(df, title)
    if err != None:
        return err

    err = saveWorkspace(df, source)
    if err != None:
        return err

    return None

def Reload(source: str):
    df, err = getWorkspace(source)
    if err != None:
        return err

    ReloadAll(df)

    err = saveWorkspace(df, source)
    if err != None:
        return err

def getKey(data: dict) -> tuple[str, Error]:
    requiredKeys = {'TITLE'}
    if not requiredKeys.issubset(data.keys()):
        return None, ErrorInvalidFormat()

    return data['TITLE'], None

def getKeys(data: dict) -> tuple[str, str, any, Error]:
    requiredKeys = {'TITLE', 'SITE', 'CHAPTER'}
    if not requiredKeys.issubset(data.keys()):
        return None, None, None, ErrorInvalidFormat()

    return data['TITLE'], data['SITE'], data['CHAPTER'], None

def getDateAndStatus(url: str, chapter: any) -> tuple[str, any]:
    status = getStatus(url, chapter)
    date = datetime.now().date()

    return status, date