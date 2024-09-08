import pandas as pd
from model.entity_scan import Scan, InstatiateScanFromDataframe


def GetAll(df: pd.DataFrame, tier: int) -> list[dict]:
    jsonList = []

    df_copy = df.copy()
    filtered_df = df_copy[df_copy['TIER'] == tier]

    for _, row in filtered_df.iterrows():
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


def Get(df: pd.DataFrame, title: str) -> dict:
    df_copy = df.copy()
    entryExist = df_copy[df_copy["TITLE"] == title]

    if entryExist.empty:
        return None

    row = entryExist.to_dict(orient='records')[0]

    return row


def Insert(df: pd.DataFrame, scan: Scan):
    df.loc[len(df.index)] = [scan.Title(), scan.URL(), scan.Chapter(), scan.Status(), scan.Tier()]


def Replace(df: pd.DataFrame, scan: Scan):
    df.loc[df["TITLE"] == scan.Title()] = [scan.Title(), scan.URL(), scan.Chapter(), scan.Status(), int(scan.Tier())]


def ReplaceStatusAll(df: pd.DataFrame):
    for _, row in df.iterrows():
        scan = InstatiateScanFromDataframe(row['TITLE'], row['SITE'], row['CHAPTER'], row['TIER'])
        df.loc[df["TITLE"] == scan.Title()] = [scan.Title(), scan.URL(), scan.Chapter(), scan.Status(), scan.Tier()]


def Remove(df: pd.DataFrame, title: str):
    df.drop(df.index[df["TITLE"] == title], inplace=True)
