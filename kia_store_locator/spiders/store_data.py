import gzip
import hashlib
import json
import os
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from urllib.parse import urlencode

from kia_store_locator.items import KiaDealerDataItem


def get_website(store_dict):
    """
    Extracts the 'website' field from the store_dict if it exists.
    Returns 'N/A' if the 'website' field is not present.
    """
    return store_dict.get('website', 'N/A')


def get_dealer_name(store_dict):
    """
    Extracts the 'dealerName' field from the store_dict if it exists.
    Returns 'N/A' if the 'dealerName' field is not present.
    """
    return store_dict.get('dealerName', 'N/A')


def get_address1(store_dict):
    """
    Extracts the 'address1' field from the store_dict if it exists.
    Returns 'N/A' if the 'address1' field is not present.
    """
    return store_dict.get('address1', 'N/A')


def get_address2(store_dict):
    """
    Extracts the 'address2' field from the store_dict if it exists.
    Returns 'N/A' if the 'address2' field is not present.
    """
    return store_dict.get('address2', 'N/A')


def get_address3(store_dict):
    """
    Extracts the 'address3' field from the store_dict if it exists.
    Returns 'N/A' if the 'address3' field is not present.
    """
    return store_dict.get('address3', 'N/A')


def get_phone1(store_dict):
    """
    Extracts the 'phone1' field from the store_dict if it exists.
    Returns 'N/A' if the 'phone1' field is not present.
    """
    return store_dict.get('phone1', 'N/A')


def get_phone2(store_dict):
    """
    Extracts the 'phone2' field from the store_dict if it exists.
    Returns 'N/A' if the 'phone2' field is not present.
    """
    return store_dict.get('phone2', 'N/A')


def get_city_code(store_dict):
    """
    Extracts the 'cityCode' field from the store_dict if it exists.
    Returns 'N/A' if the 'cityCode' field is not present.
    """
    return store_dict.get('cityCode', 'N/A')


def get_state_code(store_dict):
    """
    Extracts the 'stateCode' field from the store_dict if it exists.
    Returns 'N/A' if the 'stateCode' field is not present.
    """
    return store_dict.get('stateCode', 'N/A')


def get_latitude(store_dict):
    """
    Extracts the 'lat' field from the store_dict if it exists.
    Returns 'N/A' if the 'lat' field is not present.
    """
    return store_dict.get('lat', 'N/A')


def get_longitude(store_dict):
    """
    Extracts the 'lng' field from the store_dict if it exists.
    Returns 'N/A' if the 'lng' field is not present.
    """
    return store_dict.get('lng', 'N/A')


def get_sort_id(store_dict):
    """
    Extracts the 'sortId' field from the store_dict if it exists.
    Returns 'N/A' if the 'sortId' field is not present.
    """
    return store_dict.get('sortId', 'N/A')


def get_dealer_type(store_dict):
    """
    Extracts the 'dealerType' field from the store_dict if it exists.
    Returns 'N/A' if the 'dealerType' field is not present.
    """
    return store_dict.get('dealerType', 'N/A')


def get_dealer_id(store_dict):
    """
    Extracts the 'id' field from the store_dict if it exists.
    Returns 'N/A' if the 'id' field is not present.
    """
    return store_dict.get('id', 'N/A')


def get_email(store_dict):
    """
    Extracts the 'email' field from the store_dict if it exists.
    Returns 'N/A' if the 'email' field is not present.
    """
    return store_dict.get('email', 'N/A')


def get_city_name(store_dict):
    """
    Extracts the 'cityName' field from the store_dict if it exists.
    Returns 'N/A' if the 'cityName' field is not present.
    """
    return store_dict.get('cityName', 'N/A')


def get_state_name(store_dict):
    """
    Extracts the 'stateName' field from the store_dict if it exists.
    Returns 'N/A' if the 'stateName' field is not present.
    """
    return store_dict.get('stateName', 'N/A')


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


class StoreDataSpider(scrapy.Spider):
    name = "store_data"

    def __init__(self):
        super().__init__()
        # allowed_domains = ["abc.com"]
        # start_urls = ["https://abc.com"]

        # Connecting to Database
        self.client = pymysql.Connect(
            database='kia_db',
            user='root',
            password='actowiz',
            autocommit=True,
        )
        self.cursor = self.client.cursor()

    # Setting project name for creating separate folder for saving pages
    project_name = 'Kia_Store_Locator'
    project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
    # Creating Project files folder if not exists
    ensure_dir_exists(dir_path=project_files_dir)

    def start_requests(self) -> Iterable[Request]:
        fetch_table = 'locations_data'
        fetch_query = f'''SELECT * FROM {fetch_table};'''
        self.cursor.execute(query=fetch_query)
        rows = self.cursor.fetchall()
        print(f'Fetched {len(rows)} data.')

        for row in rows:
            state_key = row[2]
            city_key = row[4]
            base_url = 'https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do'

            query_params = {
                'state': state_key,
                'city': city_key
            }

            city_url = f'{base_url}?{urlencode(query_params)}'
            print('Working on:', city_url)
            yield scrapy.Request(
                url=city_url,
                method='POST',
                callback=self.parse
            )

    def parse(self, response):
        # Saving Page
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)
        folder_path = os.path.join(self.project_files_dir, 'Dealers_Data_Pages')
        ensure_dir_exists(dir_path=folder_path)
        file_path = os.path.join(folder_path, filename)
        with gzip.open(filename=file_path, mode='wb') as file:
            file.write(response.body)
            print('Page Saved')

        response_text = response.body.decode()
        response_dict = json.loads(response_text)
        stores_list = response_dict['data']

        # Creating an instance of Item Class
        item = KiaDealerDataItem()

        for store_dict in stores_list:
            # Extract and assign values using dedicated functions for consistency
            item['website'] = get_website(store_dict)
            item['dealer_name'] = get_dealer_name(store_dict)
            item['address1'] = get_address1(store_dict)
            item['address2'] = get_address2(store_dict)
            item['address3'] = get_address3(store_dict)
            item['phone1'] = get_phone1(store_dict)
            item['phone2'] = get_phone2(store_dict)
            item['city_code'] = get_city_code(store_dict)
            item['state_code'] = get_state_code(store_dict)
            item['latitude'] = get_latitude(store_dict)
            item['longitude'] = get_longitude(store_dict)
            item['sort_id'] = get_sort_id(store_dict)
            item['dealer_type'] = get_dealer_type(store_dict)
            item['dealer_id'] = get_dealer_id(store_dict)
            item['email'] = get_email(store_dict)
            item['city_name'] = get_city_name(store_dict)
            item['state_name'] = get_state_name(store_dict)

            yield item
            print('*' * 50)
        print('-' * 100)


if __name__ == '__main__':
    execute(f'scrapy crawl {StoreDataSpider.name}'.split())
