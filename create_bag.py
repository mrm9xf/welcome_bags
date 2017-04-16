import os
import sys
import json
import pyodbc
from settings import settings

def get_combos(connection):
    combos = {}

    query_results = settings.run_query('get_combinations', connection, {'number_of_people': 60})

    for result in query_results:
        combos[result.combination] = {
            'price_per_bag': str(result.price_per_bag),
            'total_price': str(result.total_price)
        }

    return combos

def get_items(connection):
    items = {}

    query_results = settings.run_query('get_items', connection)
    for r in query_results:
        item = {
            'item_name': r.item_name,
            'item_price': float(r.item_price),
            'item_count': r.item_count,
            'price_per_item': float(r.item_price / r.item_count),
            'item_category': r.item_category_id,
            'item_sub_category': r.item_sub_category_id
        }

        items[r.item_index] = item

    return items

def detail_bag(combo, items):
    #parse string to list
    combo = list(combo)

    num = 1
    for index, item_boolean in enumerate(combo):
        item_name = items[int(index)]['item_name']
        if int(item_boolean):
            print '{0}.\t{1}\t{2}'.format(str(num), item_name, settings.desired_count[item_name])
            num += 1

def main(connection):
    #pull items
    items = get_items(connection)

    #pull combos
    combos = get_combos(connection)

    for combo, combo_info in combos.iteritems():
        total_price = combo_info['total_price']
        price_per_bag = combo_info['price_per_bag']

        print 'Total Price: ${0}'.format(total_price)
        print 'Price Per Bag: ${0}'.format(price_per_bag)
        detail_bag(combo, items)
        break


#if __name__ == '__main__':
print('started process')
connection = settings.get_connection()
print('connection built')
main(connection)
print('finished process')
