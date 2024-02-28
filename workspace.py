from error import Error, ErrorInvalidPayload

manhwaCSV = "P:\\CSV\\manhwa.csv"
mangaCSV = "P:\\CSV\\manga.csv"

def getWorkspace(source: str) -> tuple[str, Error]:
    if source == "manhwa":
        return manhwaCSV, None
    
    elif source == "manga":
        return mangaCSV, None
    
    return None, ErrorInvalidPayload
