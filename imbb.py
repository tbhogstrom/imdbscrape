import csv

with open('input.csv', 'rb') as csvfile:
	inputreader = csv.reader(csvfile)
	for row in inputreader:
		print(row)