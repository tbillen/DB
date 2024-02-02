import configparser
import json

import requests

import Query
from MySQL import MySQL

config = configparser.ConfigParser()
config.read('config.ini')

url = "https://apis.deutschebahn.com/"

base_url = 'db-api-marketplace/apis/'

mysql = MySQL(connector=config['db'])


def get_station():
    """

    :return:
    """
    api = f"""{base_url}ris-stations/v1/stations?limit=10000"""
    params = {
        'state': 'NW',
        'locales': 'DE',

    }

    headers = {
        'DB-Client-Id': config["api"]["client_id"],
        'DB-Api-Key': config["api"]["client_secret"],
        'accept': "application/vnd.de.db.ris+json"
    }

    response = requests.get(url=url + api, headers=headers, params=params)

    print(response.status_code)
    # print(response.text)

    res = json.loads(response.text)["stations"]
    tmp = []
    for r in res:
        if "stationCategory" in r:
            tmp.append((int(r["stationID"]), r["names"]["DE"]["name"], r["stationCategory"]))
        else:
            tmp.append((int(r["stationID"]), r["names"]["DE"]["name"]))

    for item in tmp:
        get_eva(item[0])
        if len(item) > 2:
            mysql.insert(
                query=Query.insert_station(station_id=int(item[0]), name=item[1],
                                           category=int(item[2].replace("CATEGORY_", ""))))
        else:
            mysql.insert(query=Query.insert_station_without_category(station_id=int(item[0]), name=item[1]))


def get_eva(station_id: int):
    api = f"""{base_url}station-data/v2/stations/{station_id}"""

    headers = {
        'DB-Client-Id': config["api"]["client_id"],
        'DB-Api-Key': config["api"]["client_secret"],
        'accept': "application/json"
    }

    response = requests.get(url=url + api, headers=headers)

    if response.status_code == 200:
        item = json.loads(response.text)

        if 'result' in item:
            print(item["result"])
            eva = item["result"][0]["evaNumbers"]
            if len(eva) > 0:
                mysql.update(Query.update_eva(station_id, eva[0]["number"]))
        else:
            print("not found", station_id)


def main():
    """
    
    :return:
    """
    get_station()


if __name__ == '__main__':
    main()
