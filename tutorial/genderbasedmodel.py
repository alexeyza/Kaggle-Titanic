import csv as csv 
import numpy as np

test_file_obect = csv.reader(open('../csv/test.csv', 'rb'))
header = test_file_obect.next()

predictions_file = csv.writer(open("../csv/genderbasedmodelpy.csv", "wb"))
predictions_file.writerow(["PassengerId", "Survived"])

for row in test_file_obect:
    if row[3] == 'female':
        predictions_file.writerow([row[0], "1"])
    else:
        predictions_file.writerow([row[0], "0"])