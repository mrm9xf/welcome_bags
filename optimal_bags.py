import sys
import json
import random
import argparse
from math import ceil
from pprint import pprint
from settings import settings

def return_parsed_args():
    program_help = 'program to cycle through X iterations of randomly compiling and pricing '
    program_help += 'N bags for the wedding of the soon to be Mr. and Mrs. Myers'
    parser = argparse.ArgumentParser(description=program_help)

    n_bags_help = 'Number of bags anticipated for wedding (60 minimum)'
    parser.add_argument('-n', '--n_bags', dest='number_of_bags', type=int, help=n_bags_help)

    x_combos_help = 'Number of random iterations to be attempted, repeats will be skipped'
    parser.add_argument('-x', '--x_combos', dest='number_of_combos', type=int, help=x_combos_help)
    
    args = parser.parse_args()

    if args.number_of_bags < 60:
        sys.exit('Please enter a number of bags greater than 60')

    return args

def get_existing_combinations(connection, query_params):
    chosen = []

    query_results = settings.run_query('get_combinations', connection, query_params)
    for r in query_results:
        chosen.append(r.combination)

    return chosen

def get_items(connection):
    items = {}

    query_results = settings.run_query('get_items', connection)
    for r in query_results:
        item = {
            'item_name': r.item_name,
            'item_price': float(r.item_price),
            'item_count': r.item_count,
            'price_per_item': float(r.item_price / r.item_count)
        }

        items[r.item_index] = item

    return items

def price_per_bag(choices, items):
    total = 0

    for index, choice in enumerate(choices):
        if choice == 1:
            total += items[index]['price_per_item'] * settings.desired_count[items[index]['item_name']]

    return total + 8

def total_price(choices, items, number_of_people):
    total = 0

    for index, choice in enumerate(choices):
        if choice == 1:
            num_needed = number_of_people * settings.desired_count[items[index]['item_name']]
            units_needed = ceil(float(num_needed) / items[index]['item_count'])
            price = units_needed * items[index]['item_price']
            total += price

    return total + (number_of_people * 8.00)

def main(items, connection):
    choices = []
    for i in range(len(items)):
        n = settings.round(random.random())
        #print '{0},{1},{2}'.format(str(items[i]['item_name']), str(n), str(items[i]['price_per_item']))
        choices.append(n)

    return choices
        


if __name__ == '__main__':
    #get args
    args = return_parsed_args()

    #build connection
    connection = settings.get_connection()

    query_params = {'number_of_people': args.number_of_bags}

    #chosen
    chosen = get_existing_combinations(connection, query_params)
    print json.dumps(chosen)
    
    #get items
    items = get_items(connection)


    so_far = 0
    #start iterating, 10,000 times
    for i in range(args.number_of_combos):
        choices = main(items, connection)
        s = ''.join(str(x) for x in choices)
        if s in chosen:
            continue

        chosen.append(s)

        params = {
            'combination': s,
            'number_of_people': args.number_of_bags,
            'price_per_bag': price_per_bag(choices, items),
            'total_price': total_price(choices, items, args.number_of_bags)
        }

        settings.write_query('write_combo', connection, params)
        so_far += 1
        if so_far == 500:
            print '{0} combinations attempted so far'.format(str(i + 1))
            so_far = 0
