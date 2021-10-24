import requests
import json


def get_account_data(username, tagline):
    return requests.get('https://api.henrikdev.xyz/valorant/v1/account/' + username + '/' + tagline).json()


def get_mmr_data(version, region, username, tagline):
    return requests.get('https://api.henrikdev.xyz/valorant/' + version + '/mmr/' + region + '/' + username + '/' + tagline).json()


def raw(category, region, puuid, queries):
    return requests.post('https://api.henrikdev.xyz/valorant/v1/raw', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": category, "value": puuid, "region": region, "queries": queries})).json()


def get_match_data(match_id):
    return requests.get('https://api.henrikdev.xyz/valorant/v2/match/' + match_id).json()


def get_mmr_data_by_puuid(version, region, puuid):
    return requests.get('https://api.henrikdev.xyz/valorant/' + version + '/by-puuid/mmr/' + region + '/' + puuid).json()


def get_total(region, puuid):
    return requests.post('https://api.henrikdev.xyz/valorant/v1/raw', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": "matchhistory", "value": puuid, "region": region})).json()["Total"]


def get_matchhistory(region, puuid,total, match):
    if match <= total:
        matchid = requests.post('https://api.henrikdev.xyz/valorant/v1/raw', headers={'Content-Type': 'application/json'}, data=json.dumps({"type": "matchhistory", "value": puuid, "region": region, "queries": "?&startIndex=" + str(match - 1) + "&endIndex=" + str(match)})).json()["History"][0]["MatchID"]
        return get_match_data(matchid)
    else:
        return False


def get_rank_icon(currenttier):
    length = len(requests.get('https://valorant-api.com/v1/competitivetiers').json()["data"]) - 1
    uuid = requests.get('https://valorant-api.com/v1/competitivetiers').json()["data"][length]["uuid"]
    return "https://media.valorant-api.com/competitivetiers/" + uuid + "/" + str(currenttier) + "/largeicon.png"


def get_map_data(name):
    maps = requests.get('https://valorant-api.com/v1/maps').json()
    for map in maps["data"]:
        if map["displayName"] == name:
            return map


def get_playertitle(puuid):
    return requests.get('https://valorant-api.com/v1/playertitles/' + puuid).json()
