import csv
import os

def get_test_data():
    """
    Reads test input from a CSV file.
    Returns a dictionary containing search query, max price, and item limit.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.csv')
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)[0]