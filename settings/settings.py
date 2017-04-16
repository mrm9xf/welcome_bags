import os
import sys
import pyodbc

DIR_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
QUERIES_DIR = os.path.join(DIR_LOCATION, 'queries')

# Help Remembering Table Columns

# Table #1: welcome_bags.items
# 1. item_index
# 2. item_name
# 3. item_price
# 4. item_count
# 5. item_category_id
# 6. item_sub_category_id

# Table #2: welcome_bags.bag_combinations
# 1. combination
# 2. number_of_people
# 3. price_per_bag
# 4. total_price

desired_count = {
    'Deer Park Water': 1,
    'Gatorade': 1,
    'Hershey\'s Kisses': 5,
    'Lindt Truffles': 5,
    'Fruit Snacks': 2,
    'Nutella Go Packs': 1,
    'Frito Lay Variety': 1,
    'Pringles': 1,
    'Life Savers': 5,
    'Trail Mix': 1,
    'Oreos': 1,
    'Double Mint Gum': 1,
    'Fruit by the foot': 2,
    'Starburst': 1,
    'Skittles': 1,
    'Nutrigrain bars': 1,
    'Rice Krispeys': 1,
    'Utz Variety': 1,
    'Utz Salted': 1,
    'Spindrift': 1,
    'Caprisun': 1,
    'Cheezitz': 1,
    'York Peppermint Patty': 3,
    'Cliff Bar': 1,
    'Goldfish': 1,
    'Nature Valley Peanut': 1,
    'Popcorn': 1
}

def get_connection():
    connection = pyodbc.connect('DSN=MYSQL')
    return connection

def round(x):
    return int(x + 0.5)

def run_query(query_name, connection, params=None):
    sql = open(os.path.join(QUERIES_DIR, query_name + '.sql'), 'r').read()

    if params:
        sql = sql.format(**params)

    results = connection.cursor().execute(sql).fetchall()

    return results

def write_query(query_name, connection, params=None):
    if params is None:
        sys.exit('Please supply parameters when executing {0}.sql'.format(query_name))

    sql = open(os.path.join(QUERIES_DIR, query_name + '.sql'), 'r').read().format(**params)

    connection.cursor().execute(sql)
    connection.commit()
