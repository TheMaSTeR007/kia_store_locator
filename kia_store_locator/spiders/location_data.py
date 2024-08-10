import json
import os
import gzip
import hashlib
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from kia_store_locator.items import KiaStoreLocatorItem


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


class LocationDataSpider(scrapy.Spider):
    name = "location_data"
    # allowed_domains = ["xyz.com"]
    # start_urls = ["https://xyz.com"]

    def __init__(self):
        super().__init__()

        # Connecting to Database
        self.client = pymysql.Connect(
            database='kia_db',
            user='root',
            password='actowiz',
            autocommit=True,
        )
        self.cursor = self.client.cursor()

    # Defining start urls to start requesting from
    start_urls = ["https://www.kia.com/api/kia2_in/findAdealer.getStateCity.do"]

    # Setting project name for creating separate folder for saving pages
    project_name = 'Kia_Store_Locator'
    project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
    # Creating Project files folder if not exists
    ensure_dir_exists(dir_path=project_files_dir)


    def parse(self, response):
        # Saving Page
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)
        ensure_dir_exists(dir_path=os.path.join(self.project_files_dir, 'location_data_Page'))
        file_path = os.path.join(self.project_files_dir, 'location_data_Page', filename)
        with gzip.open(filename=file_path, mode='wb') as file:
            file.write(response.body)
            print('Page Saved')

        # Creating an instance of Item Class
        location_data_item = KiaStoreLocatorItem()

        # Retrieving locations dictionaries from json for extracting data from each of them
        dict_data = json.loads(response.body.decode())
        state_city_list = dict_data['data']['stateAndCity']
        for state_city in state_city_list:
            state_dict = state_city['val1']
            state_name = state_dict['value']
            state_key = state_dict['key']
            cities_dict_list = state_city['val2']
            for city in cities_dict_list:
                city_name = city['value']
                city_key = city['key']
                city_url = f'https://www.kia.com/api/kia2_in/findAdealer.getDealerList.do?state={state_key}&city={city_key}'
                print(
                    'State Name:', state_name,
                    'State Key:', state_key, '\n',
                    'City Name:', city_name,
                    'City Key:', city_key,
                    'City Url:', city_url
                )
                location_data_item['state_name'] = state_name
                location_data_item['state_key'] = state_key
                location_data_item['city_name'] = city_name
                location_data_item['city_key'] = city_key
                location_data_item['city_url'] = city_url
                yield location_data_item
                print('-'*100)


if __name__ == '__main__':
    execute(f'scrapy crawl {LocationDataSpider.name}'.split())

