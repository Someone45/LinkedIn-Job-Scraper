# open('jobdesc.txt', 'w').close()
# open('jobtitle.txt', 'w').close()
import tabulate
import csv

with open('datafile.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(content2)
    