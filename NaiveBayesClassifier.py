from csv import reader
from random import seed
from random import randrange
from math import sqrt
from math import exp
from math import pi


def load_dataset(filename, relevantcolumns):
    dataset = list()
    firstline = True
    invalidData = False
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if firstline:
                firstline = False
                continue
            for i in relevantcolumns:
                if(i == 7):
                    continue
                if(int(row[i]) == 97 or int(row[i]) == 98 or int(row[i]) == 99):
                    invalidData = True
                    break
            if invalidData:
                invalidData = False
                continue
            if not row:
                continue
            dataset.append(row)
    return dataset

def clean_data(dataset, relevantcolumns):
    cleandata = list()
    for x in range(len(dataset)):
        for i in relevantcolumns:
            cleandata[x].append(dataset[relevantcolumns])
    return cleandata


def split_posneg(dataset): #0 is for negative cases 1 is for positive cases
    split = dict()
    split[0] = list()
    split[1] = list()
    for i in range(len(dataset)):
        vector = dataset[i]
        posneg = vector[4]
        if(posneg == "9999-99-99"):
            split[0].append(vector)
        else:
            split[1].append(vector)
    return split


def stats(data):
    avg = 0
    for i in data:
        avg = avg + int(i)
    avg = avg/float(len(data))
    var = 0
    for i in range(len(data)):
        var = var + (int(data[i])-avg)**2
    var = var/float(len(data)-1)
    stddev = sqrt(var)
    return avg, stddev

def dataset_stats(dataset, relevant_columns):
    column_count = 0
    columns = dict()
    datastats = list()
    for i in relevant_columns:
        columns[column_count] = list()
        for x in range(len(dataset)):
            columns[column_count].append(dataset[x][i])
        average, standarddev = stats(columns[column_count])
        datastats.append([average, standarddev, len(columns[column_count])])
        column_count+=1
    return datastats

def posneg_stats(dataset, relevantcolumns):
    split = split_posneg(dataset)
    posnegstats = dict()
    posnegstats[0] = list()
    posnegstats[1] = list()
    posnegstats[0] = (dataset_stats(split[0], relevantcolumns))
    posnegstats[1] = (dataset_stats(split[1], relevantcolumns))
    return posnegstats

def calculate_probabilities(x, avg, stddev):
    exponent = exp(-((x-avg)**2/(2*stddev**2)))
    pdf = (1/(sqrt(2*pi)*stddev))*exponent
    return pdf

def calculate_class_probabilities(posnegstats, entry, relevantcolumns):
    num_entries = posnegstats[0][2][2] + posnegstats[1][2][2]
    probabilities = dict()
    probabilities[0] = list()
    probabilities[1] = list()
    for i in range(2):
        probabilities[i] = posnegstats[i][0][2]/float(num_entries)
        for x in range(len(posnegstats[i])):
            avg, stddev, count = posnegstats[i][x]
            probabilities[i] *= calculate_probabilities(int(entry[x]), avg, stddev)
    return probabilities

 


relevantcolumns = [6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20]
filename = 'covid_train.csv'
dataset = load_dataset(filename, relevantcolumns)
splitdata = split_posneg(dataset)
#for i in range(10):
#    print(dataset[i])
#for i in range(10):
#    print(splitdata[1][i][4])


data = [1,2,3,4,5,6,7,8]
average, standarddev = stats(data)
print(average)
print(standarddev)
datastats = dataset_stats(dataset, relevantcolumns)
posnegstats = posneg_stats(dataset, relevantcolumns)
#print(posnegstats[0])
#print(posnegstats[0][1])
#print(posnegstats[0][1][2])
#print(posnegstats[1])
probabilities = calculate_class_probabilities(posnegstats, dataset[0], relevantcolumns)
print(probabilities)
