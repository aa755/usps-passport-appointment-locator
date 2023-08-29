import time

import requests
import json
import argparse
import datetime
import requests
import os
import csv
from io import StringIO

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
        "--radius",
        dest="radius",
        action="store",
        help="radius in miles to search around zipcode.",
        default="20",
    )
    parser.add_argument(
        "--max-date",
        dest="max_date",
        action="store",
        help="maximum date to search for appointments",
    )

    return parser.parse_args()

def get_post_response(url:str, payload:str):
    headers = {
    'User-Agent': 'Mozilla/5.0',
      'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response
def get_location_ids(zip_code:str, radius:str)->tuple[list, list]:
    today_date  = datetime.datetime.today().strftime('%Y%m%d')

    url = "https://tools.usps.com/UspsToolsRestServices/rest/v2/facilityScheduleSearch"
    payload = json.dumps({
        "poScheduleType": "PASSPORT",
        "date": today_date,
        "numberOfAdults": "0",
        "numberOfMinors": "1",
        "radius": radius,
        "zip5": zip_code,
        "city": "",
        "state": ""
    })

    response = get_post_response(url, payload)
    ids = []
    address = []
    for foo in response.json()['facilityDetails']:
        ids.append(foo['fdbId'])
        address.append(foo['address'])
    return ids, address


def get_zip_codes_within_radius(zip_code, distance, units='miles'):
    """
    Fetches a list of zip codes within a given radius of the provided zip code.

    :param zip_code: The target zip code.
    :param distance: The radius.
    :param units: The unit of measure (default is 'miles').
    :return: A list of dictionaries with zip code details.
    """

    API_ENDPOINT = "https://www.zipcodeapi.com/rest/{api_key}/radius.csv/{zip_code}/{distance}/{units}"
    API_KEY = os.environ.get("ZIP_RADIUS_API_KEY")

    if not API_KEY:
        raise ValueError("ZIP_RADIUS_API_KEY environment variable not set.")

    url = API_ENDPOINT.format(api_key=API_KEY, zip_code=zip_code, distance=distance, units=units)
    response = requests.get(url)

    # Check if the response is valid
    response.raise_for_status()

    # Parse CSV response
    reader = csv.DictReader(StringIO(response.text))

    return [row for row in reader]

def main():
    args = parse_args()
    polling_interval = int(args.polling_interval)
    zip_code = args.zip_code
    radius = args.radius
    # id search
    maximum_date = args.max_date
    if not maximum_date:
        maximum_date = datetime.datetime.today() + datetime.timedelta(days=30)
        maximum_date = maximum_date.strftime('%Y%m%d')


    result = get_zip_codes_within_radius(zip_code, radius)
    for zip in result:
        print(zip)
    uniq_locations={}
    num_locs=len(result)
    count = 0
    for zip in result:
        print(f"{count}/{num_locs}: considering locations near zip {zip}")
        count = count+1
        ids, addresses = get_location_ids(zip['zip_code'], radius)
        for ii in range(len(ids)):
            locid = ids[ii]
            address=addresses[ii]
            print(f"evaluating location{locid} at address {address['addressLineOne']}, {address['city']}")
            if locid not in uniq_locations:
                uniq_locations[locid] = address
                print(f"will consider location{locid} at address {address['addressLineOne']}, {address['city']}")
        with open('.usps_passport_locator_locations_dskkaj903890jlkjafljlkdjslkafjkjc', 'w') as f:
            json.dump(uniq_locations,f) # on future runs, we can skip the above # TODO: unindent this and prev line one tab. this just for a test

    url = "https://tools.usps.com/UspsToolsRestServices/rest/v2/appointmentDateSearch"


    while True:
        for locid in uniq_locations:
            payload = json.dumps({
              "numberOfAdults": "0",
              "numberOfMinors": "1",
              "fdbId": locid,
              "productType": "PASSPORT"
            })

            response =  get_post_response(url, payload)
            address = uniq_locations[locid]

            if dates:=response.json().get("dates"):
                for date in dates:
                    if int(date) < int(maximum_date):
                        print(f"found date {date} at {address['addressLineOne'], address['city']}")

        print(f"will check again in {polling_interval}s")
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
