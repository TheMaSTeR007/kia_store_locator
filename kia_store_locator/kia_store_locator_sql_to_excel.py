import os

import pandas as pd
import pymysql

# # Creating a connection to SQL Database
connection = pymysql.connect(host='localhost', user='root', database='kia_db', password='actowiz', charset='utf8mb4', autocommit=True)

fetch_query = '''SELECT * FROM kia_dealers_data;'''  # Query that will retrieve all data from Database table


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


# Setting project name for creating separate folder for saving pages
project_name = 'Kia_Store_Locator'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files\\Output_Files'
# Creating Project files folder if not exists
ensure_dir_exists(dir_path=project_files_dir)

excel_path = project_files_dir
# Create Excel file form SQL data
dataframe = pd.read_sql(sql=fetch_query, con=connection)
writer = pd.ExcelWriter(
    path=excel_path + r'\kia_dealers_data.xlsx',
    engine='xlsxwriter',
    engine_kwargs={'options': {'strings_to_urls': False}}
)
dataframe.to_excel(excel_writer=writer)

dataframe.to_excel(writer)
writer.close()
