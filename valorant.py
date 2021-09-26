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
