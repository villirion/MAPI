import pandas as pd
from query import get_status, check_valid
from datetime import datetime

def setupCSV(csv: str) -> pd.DataFrame:
    df = pd.read_csv(csv)

    return df

def updateCSV(df: pd.DataFrame, csv: str) -> pd.DataFrame:
    df.to_csv(csv, index=False)

def List(csv: str) -> list[dict]:
    df = setupCSV(csv)

    json_list = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        json_list.append(row_dict)

    return json_list

def Get(csv: str, title: str) -> tuple[dict, int]:
    df = setupCSV(csv)

    filter_df = df[df["TITLE"] == title]

    if filter_df.empty:
        return {'ERROR': 'not found'}, 404

    row = filter_df.iloc[0]
    jsonRow = row.to_dict()

    return jsonRow, 200

def Post(csv: str, data: dict) -> tuple[dict, int]:
    df = setupCSV(csv)

    required_keys = {'TITLE', 'SITE', 'CHAPTER'}
    if not required_keys.issubset(data.keys()):
        return  {'ERROR': 'Invalid data format'}, 400

    title = data['TITLE']
    url = data['SITE']
    chapter = data['CHAPTER']

    if not check_valid(url, chapter):
        return {'ERROR': 'Invalid payload'}, 400

    status = get_status(url, chapter)
    date = datetime.now().date()

    new_entry = {'TITLE': title, 'SITE': url, 'CHAPTER': chapter, 'STATUS': status, 'LAST_UPDATE': date}
    df.loc[len(df.index)] = new_entry

    updateCSV(df, csv)

    return new_entry, 200

def Update(csv: str, data: dict) -> tuple[dict, int]:
    df = setupCSV(csv)
    df_copy = df.copy()

    required_keys = {'TITLE', 'SITE', 'CHAPTER'}
    if not required_keys.issubset(data.keys()):
        return {'ERROR': 'Invalid data format'}, 400

    title = data['TITLE']

    filter_df = df_copy[df_copy["TITLE"] == title]

    if filter_df.empty:
        return {'ERROR': 'not found'}, 404

    url = data['SITE']
    chapter = data['CHAPTER']

    if not check_valid(url, chapter):
        return {'ERROR': 'Invalid payload'}, 400

    status = get_status(url, chapter)
    date = datetime.now().date()

    updated_entry = {'TITLE': title, 'SITE': url, 'CHAPTER': chapter, 'STATUS': status, 'LAST_UPDATE': date}
    df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

    updateCSV(df, csv)

    return updated_entry, 200

def Reload(csv: str) -> tuple[dict, int]:
    df = setupCSV(csv)

    for _, row in df.iterrows():
        title = row['TITLE']
        url = row['SITE']
        chapter = row['CHAPTER']
        status = get_status(url, chapter)
        date = datetime.now().date()
        df.loc[df["TITLE"] == title] = [title, url, chapter, status, date]

    updateCSV(df, csv)

    return {}, 200

def Delete(csv: str, data: dict) -> tuple[dict, int]:
    df = setupCSV(csv)
    df_copy = df.copy()

    required_keys = {'TITLE'}
    if not required_keys.issubset(data.keys()):
        return  {'ERROR': 'Invalid data format'}, 400

    title = data['TITLE']

    filter_df = df_copy[df_copy["TITLE"] == title]

    if filter_df.empty:
        return {'ERROR': 'not found'}, 404

    df = df.drop(df.index[df["TITLE"] == title])

    updateCSV(df, csv)

    return {}, 200