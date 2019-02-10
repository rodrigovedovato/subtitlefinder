from hasher import hashFile
from utils import toJson

import os

def sortByScore(e):
    return e["Score"]

ranks = {
    "ANONYMOUS" : 0,
    "SUBLEECHER" : 1,
    "VIPMEMBER" : 2,
    "BRONZEMEMBER" : 3,
    "SILVERMEMBER" : 4,
    "GOLDMEMBER" : 5,
    "PLATINUMMEMBER" : 6,
    "TRUSTED" : 7,
    "ADMINISTRATOR" : 8,
    "TRANSLATOR" : 9
}

def normalizeDownloadCount(ranking):
    if ranking <= 0:
        return 0
    elif ranking > 0 and ranking <= 12500:
        return 1        
    elif ranking >= 12501 and ranking <= 25000:
        return 2
    elif ranking >= 25001 and ranking <= 37500:
        return 3
    elif ranking >= 37501 and ranking <= 50000:
        return 4
    elif ranking >= 50001 and ranking <= 62500:
        return 5
    elif ranking >= 62500 and ranking <= 75000:
        return 6
    elif ranking >= 75001 and ranking <= 87500:
        return 7
    elif ranking >= 87501 and ranking <= 100000:
        return 8
    else:
        return 9
    
def normalizeRating(rating):
    if (rating <= 0):
        return 0
    else:
        return rating - 1

def transformFullTextResults(subtitle):
    return {
        "userRank" : ranks[subtitle["UserRank"].upper().replace(" ","")],
        "downloadCount" : normalizeDownloadCount(int(subtitle["SubDownloadsCnt"])),
        "rating" : normalizeRating(float(subtitle["SubRating"])),
        "link" : subtitle["ZipDownloadLink"]
    }

def exactSearch(os_client, file_name, token, language):       
    results = os_client.SearchSubtitles(token, [
        {
            "moviehash" : hashFile(file_name),
            "moviebytesize" : str(os.path.getsize(file_name)),
            "sublanguageid" :  language
        }
    ])

    subtitle_data = toJson(results)
    return subtitle_data["data"].sort(key=sortByScore,reverse=True)[0]["ZipDownloadLink"]


def searchByAttributeRanking(e):
    return e["userRank"] * 100 + e["downloadCount"] * 10 + e["rating"]

def textSearch(os_client, file_name, token, language):
    basename = os.path.basename(file_name)
    results = os_client.SearchSubtitles(token, [
        {
            "query" : os.path.splitext(basename)[0],
            "sublanguageid" :  language
        }
    ])

    transformed_results = [ transformFullTextResults(x) for x in results["data"] if x["SubFromTrusted"] == "1" ]
    return transformed_results.sort(key=searchByAttributeRanking,reverse=True)[0]["link"]