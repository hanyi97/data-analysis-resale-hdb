import csv

CONST_filename = 'resale_flat_prices.csv'


# Reads data from CSV and returns a list
# Note that first item in list are the columns of the dataset
def get_data():
    with open(CONST_filename, 'r', encoding='utf-8-sig') as csv_file:
        return list(csv.reader(csv_file, delimiter=','))


# Reads data from CSV and returns it as a list of dictionaries
def get_dict_data():
    with open(CONST_filename, 'r', encoding='utf-8-sig') as csv_file:
        return list(csv.DictReader(csv_file, delimiter=','))
