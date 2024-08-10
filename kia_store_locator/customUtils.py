# Dynamic Insert query
def insert_into(table_name, cols, placeholders):
    insert_query = f'''INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders});'''
    return insert_query


locations_data_table_query = '''CREATE TABLE locations_data (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                state_name VARCHAR(255),
                                state_key VARCHAR(255),
                                city_name VARCHAR(255),
                                city_key VARCHAR(255),
                                city_url VARCHAR(255)
                                );'''

kia_dealers_data_table_query = '''CREATE TABLE kia_dealers_data (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    dealer_name VARCHAR(255),
                                    address1 VARCHAR(255),
                                    address2 VARCHAR(255),
                                    address3 VARCHAR(255),
                                    phone1 VARCHAR(255),
                                    phone2 VARCHAR(255),
                                    website VARCHAR(255),
                                    state_name VARCHAR(255),
                                    city_name VARCHAR(255),
                                    city_code VARCHAR(255),
                                    state_code VARCHAR(255),
                                    latitude VARCHAR(255),
                                    longitude VARCHAR(255),
                                    sort_id VARCHAR(255),
                                    dealer_type VARCHAR(255),
                                    dealer_id VARCHAR(255),
                                    email VARCHAR(255)
                                    );'''
