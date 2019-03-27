# -*- coding: utf-8 -*-
# Author: Jakub Kubik
# Date: 27.03.2019

import argparse
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
from typing import Union


def parse_arguments() -> argparse.Namespace:
    """ Return parsed program arguments in argparse.Namespace. """
    parser = argparse.ArgumentParser()
    parser.add_argument('--cities', action='store_true', dest='cities',
                        help='Cities with airport.')
    parser.add_argument('--coords', action='store_true', dest='coords',
                        help='Coordinates of each airports.')
    parser.add_argument('--iata', action='store_true', dest='iata',
                        help='IATA codes.')
    parser.add_argument('--names', action='store_true', dest='names',
                        help='Name of the airport.')
    parser.add_argument('--full', action='store_true', dest='full',
                        help='Print every detail from each airport.')
    return parser.parse_args()


def get_airports_data_from_web_page() -> Union[None, BeautifulSoup]:
    """ Get whole web page with all airports in UK.
        If success return it else return None.
    """
    url = 'https://www.prokerala.com/travel/airports/united-kingdom/'
    try:
        response = get(url)
    except RequestException:
        return None
    bs = BeautifulSoup(response.text, 'html.parser')
    return bs


def get_lat_long_from_kiwi_api() -> Union[None, dict]:
    """ API is from task recommendation.
        Get latitudes and longitudes of supported airports by kiwi.com.
        This data are chosen according UK max, min latitude and longitude.
        If success return dict with all lat and long else return None.
    """
    url = 'https://api.skypicker.com/locations/'
    try:
        headers = {'Content-Type': 'application/json'}
        params = {'type': 'box', 'location_types': 'airport',
                  'low_lat': 50, 'high_lat': 61,
                  'low_lon': -8, 'high_lon': 2}
        response = get(url, headers=headers, params=params)
    except RequestException:
        return None
    try:
        return json.loads(response.text)
    except ValueError:
        return None


def create_structure(bs: BeautifulSoup, lat_and_long: dict) -> dict:
    """ Create dictionary of airports in UK and return it.
        In dictionary city is key, value is list which contains dictionaries
        with data to each airport (airport name, IATA code, latitude and longitude).
        Latitude and longitude is set if that airport is in kiwi api
        else latitude and longitude is set to None.
    """
    airports = dict()
    lat_lon_dict = dict()
    for coord in lat_and_long['locations']:
        lat_lon_dict[coord['code']] = {'lat': coord['location']['lat'],
                                                   'lon': coord['location']['lon']}

    for table in bs.find_all('table'):
        for row in table.find_all('tr'):
            if row.find(class_='airport-name'):

                city = row.span.text
                airport_name = row.a.text
                iata = row.find(class_='tc td-width-60').text

                latitude = longitude = None
                if iata in lat_lon_dict.keys():
                    latitude = lat_lon_dict[iata]['lat']
                    longitude = lat_lon_dict[iata]['lon']

                if city not in airports:
                    airports[city] = list()
                airports[city].append({'airport name': airport_name,
                                       'IATA': iata, 'lat': latitude, 'lon': longitude})
    return airports


def format_output(params: argparse.Namespace, airports: dict):
    """ Display all airports to stdout.
        Display them according program parameters.
    """
    # None program parameters
    if params.cities is False and \
       params.coords is False and \
       params.iata is False and \
       params.names is False and \
       params.full is False:
        for k, v in airports.items():
            for item in v:
                print(item['airport name'], end=', ')
                print(item['IATA'], end=', ')
                print()

    # --full program parameter
    elif params.full:
        for k, v in airports.items():
            for item in v:
                print(k, end=', ')
                print(item['airport name'], end=', ')
                print(item['IATA'], end=', ')
                print(item['lat'], end=', ')
                print(item['lon'], end=',')
                print()

    # other parameters and their combinations
    else:
        for k, v in airports.items():
            for item in v:
                if params.cities:
                    print(k, end=', ')
                if params.names:
                    print(item['airport name'], end=', ')
                if params.iata:
                    print(item['IATA'], end=', ')
                if params.coords:
                    print(item['lat'], end=', ')
                    print(item['lon'], end=', ')
                print()


if __name__ == '__main__':
    args = parse_arguments()

    data = get_airports_data_from_web_page()
    if data is None:
        raise SystemExit(3)

    all_lat_and_lon_uk = get_lat_long_from_kiwi_api()
    if all_lat_and_lon_uk is None:
        raise SystemExit(4)

    airports = create_structure(data, all_lat_and_lon_uk)

    format_output(args, airports)
