from model.entity_error import Error, ErrorInvalidPayload, ErrorInvalidFormat
from model.entity_scan import Scan, NewScan, NewScanFromDatabase
from model.entity_workspace import getWorkspace
from dataframe import Insert, GetAll, Exist, Replace, ReplaceStatusAll, Remove, Get
from model.entity_site import getSite
from model.entity_status import StatusLinkBroken

def List(source: str, tier: str) -> list[dict]:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    return GetAll(workspace.DF(), int(tier))


def Post(source: str, data: dict) -> Error:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    scan, err = createScan(data)
    if err is not None:
        return err

    Insert(workspace.DF(), scan)

    workspace.Save()

    return None


def Update(source: str, data: dict) -> Error:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    scan, err = createScan(data)
    if err is not None:
        return err

    if not Exist(workspace.DF(), scan.Title()):
        return ErrorInvalidPayload()

    Replace(workspace.DF(), scan)

    workspace.Save()

    return None


def Delete(source: str, data: dict) -> Error:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    title, err = getTitle(data)
    if err is not None:
        return err

    if not Exist(workspace.DF(), title):
        return ErrorInvalidPayload()

    Remove(workspace.DF(), title)

    workspace.Save()

    return None


def Reload(source: str, data: dict) -> Error:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    title, err = getTitle(data)
    if err is not None:
        return err

    scan = Get(workspace.DF(), title)
    if scan is None:
        return ErrorInvalidPayload()

    if scan['STATUS'] == StatusLinkBroken().String():
        site, _ = getSite(scan['SITE'])
        newSite = site.reloadURL(scan['TITLE'])
        if newSite is not None:
            scan['SITE'] = newSite

    updatedScan = NewScanFromDatabase(scan['TITLE'], scan['SITE'], scan['CHAPTER'], scan['TIER'])

    Replace(workspace.DF(), updatedScan)

    workspace.Save()

    return None


def ReloadAll(source: str) -> Error:
    workspace, err = getWorkspace(source)
    if err is not None:
        return err

    ReplaceStatusAll(workspace.DF())

    workspace.Save()

    return None


def getTitle(data: dict) -> tuple[str, Error]:
    requiredKeys = {'TITLE'}
    if not requiredKeys.issubset(data.keys()):
        return None, ErrorInvalidFormat()

    return data['TITLE'], None

def createScan(data: dict) -> tuple[Scan, Error]:
    requiredKeys = {'TITLE', 'SITE', 'CHAPTER', 'TIER'}
    if not requiredKeys.issubset(data.keys()):
        return None, ErrorInvalidFormat()

    return NewScan(data['TITLE'], data['SITE'], data['CHAPTER'], data['TIER'])
