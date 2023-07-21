import time

import requests
import json
import argparse
import datetime

def parse_args():
    parser = argparse.ArgumentParser(
    )

    parser.add_argument(
        "--polling-interval",
        dest="polling_interval",
        action="store",
        help="how often to poll for appointments",
        default=300,
    )
    parser.add_argument(
        "--zip-code",
        dest="zip_code",
        action="store",
        help="zip code to search for appointments",
        default="94085",
    )
    parser.add_argument(
        "--max-date",
        dest="max_date",
        action="store",
        help="maximum date to search for appointments",
    )
    parser.add_argument("--monitor", dest="monitor", action="store_true")
    parser.add_argument("--edit", dest="edit", action="store_true")
    parser.add_argument("--ws_id", dest="ws_id", action="store")

    return parser.parse_args()

def get_post_response(url:str, payload:str):
    headers = {
    'User-Agent': 'Mozilla/5.0',
      'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response
def get_location_ids(zip_code:str)->tuple[list, list]:
    today_date  = datetime.datetime.today().strftime('%Y%m%d')

    url = "https://tools.usps.com/UspsToolsRestServices/rest/v2/facilityScheduleSearch"
    payload = json.dumps({
        "poScheduleType": "PASSPORT",
        "date": today_date,
        "numberOfAdults": "0",
        "numberOfMinors": "1",
        "radius": "20",
        "zip5": zip_code,
        "city": "",
        "state": ""
    })

    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    #   'Content-Type': 'application/json',
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    response = get_post_response(url, payload)
    ids = []
    address = []
    for foo in response.json()['facilityDetails']:
        ids.append(foo['fdbId'])
        address.append(foo['address'])
    return ids, address

def main():
    args = parse_args()
    polling_interval = int(args.polling_interval)
    zip_code = args.zip_code
    # id search
    maximum_date = args.max_date
    if not maximum_date:
        maximum_date = datetime.datetime.today() + datetime.timedelta(days=30)
        maximum_date = maximum_date.strftime('%Y%m%d')


    ids, address = get_location_ids(zip_code)
    print(f"checking in {len(ids)} locations near zip code {zip_code} upto date: {maximum_date}")
    url = "https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentDateSearch"


    while True:
        for ii in range(len(ids)):
            payload = json.dumps({
              "numberOfAdults": "0",
              "numberOfMinors": "1",
              "fdbId": ids[ii],
              "productType": "PASSPORT"
            })

            response =  get_post_response(url, payload)

            if dates:=response.json().get("dates"):
                for date in dates:
                    if int(date) < int(maximum_date):
                        print(f"found date {date} at {address[ii]['addressLineOne'], address[ii]['city']}")

        print(f"will check again in {polling_interval}s")
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()