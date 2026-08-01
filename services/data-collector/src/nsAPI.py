from enum import Enum
import urllib.request
import json
import os

BASE_URL = "https://gateway.apiportal.ns.nl"

class Method(Enum):
    GET = 'GET'
    POST = 'POST'

def send_request(url:str, method:Method = Method.GET) -> str|None:
    header = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': os.getenv('NS_API_KEY'),
    }

    try:
        req = urllib.request.Request(url, headers=header)
        req.get_method = lambda: method.value
        response = urllib.request.urlopen(req)

        #TODO: Handle HTML responce codes

        return response.read()
    except Exception as e:
        print(e)
        return None

def get_arrivals(uicCode:str):
    url = f"{BASE_URL}/reisinformatie-api/api/v2/arrivals?uicCode={uicCode}"

    res = send_request(url)

    if (res == None):
        print(f"No data arrived from API request (url: {url})")
        return
    
    data:dict = json.loads(res)
    if (not data.get("payload")):
        print(f"No payload in API request (url: {url})")
        return

    return data["payload"]

def get_departures(uicCode:str):
    url = f"{BASE_URL}/reisinformatie-api/api/v2/departures?uicCode={uicCode}"

    res = send_request(url)

    if (res == None):
        print(f"No data arrived from API request (url: {url})")
        return
    
    data:dict = json.loads(res)
    if (not data.get("payload")):
        print(f"No payload in API request (url: {url})")
        return

    return data["payload"]

def get_stations():
    url = f"{BASE_URL}/reisinformatie-api/api/v2/stations?countryCodes=NL"

    res = send_request(url)
    
    if (res == None):
        print(f"No data arrived from API request (url: {url})")
        return
    
    data:dict = json.loads(res)
    if (not data.get("payload")):
        print(f"No payload in API request (url: {url})")
        return

    return data["payload"]
    