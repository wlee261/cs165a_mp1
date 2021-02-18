from csv import reader
from random import seed
from random import randrange
from math import sqrt
from math import exp
from math import pi


def load_dataset(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset


filename = 'C:\Users\yodal\Downloads\mp1\covid_valid.csv'
dataset = load_dataset(filename)
print(dataset[0])
