import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

csv_file_object = csv.reader(open('../csv/train.csv', 'rb'))
header = csv_file_object.next()
train_data=[]
for row in csv_file_object:
    train_data.append(row[1:])
train_data = np.array(train_data)

#Male = 1, female = 0:
train_data[train_data[0::,3]=='male',3] = 1
train_data[train_data[0::,3]=='female',3] = 0
#embark c=0, s=1, q=2
train_data[train_data[0::,10] =='C',10] = 0
train_data[train_data[0::,10] =='S',10] = 1
train_data[train_data[0::,10] =='Q',10] = 2

#All the ages with no data make the median of the data
train_data[train_data[0::,4] == '',4] = np.median(train_data[train_data[0::,4] != '',4].astype(np.float))
#All missing ebmbarks just make them embark from most common place
train_data[train_data[0::,10] == '',10] = np.round(np.mean(train_data[train_data[0::,10] != '',10].astype(np.float)))

train_data = np.delete(train_data,[2,7,9],1)

test_file_object = csv.reader(open('../csv/test.csv', 'rb'))
header = test_file_object.next()
test_data=[]
ids = []
for row in test_file_object:
    ids.append(row[0])
    test_data.append(row[1:])
test_data = np.array(test_data)


#Male = 1, female = 0:
test_data[test_data[0::,2]=='male',2] = 1
test_data[test_data[0::,2]=='female',2] = 0
#ebark c=0, s=1, q=2
test_data[test_data[0::,9] =='C',9] = 0
test_data[test_data[0::,9] =='S',9] = 1
test_data[test_data[0::,9] =='Q',9] = 2

#All the ages with no data make the median of the data
test_data[test_data[0::,3] == '',3] = np.median(test_data[test_data[0::,3] != '',3].astype(np.float))
#All missing ebmbarks just make them embark from most common place
test_data[test_data[0::,9] == '',9] = np.round(np.mean(test_data[test_data[0::,9] != '',9].astype(np.float)))
#All the missing prices assume median of their respectice class
for i in xrange(np.size(test_data[0::,0])):
    if test_data[i,7] == '':
        test_data[i,7] = np.median(test_data[(test_data[0::,7] != '') & (test_data[0::,0] == test_data[i,0]) ,7].astype(np.float))

test_data = np.delete(test_data,[1,6,8],1) #remove the name data, cabin and ticket

print 'Training'
forest = RandomForestClassifier(n_estimators=100)

forest = forest.fit(train_data[0::,1::],train_data[0::,0])

print 'Predicting'
output = forest.predict(test_data)

open_file_object = csv.writer(open("../csv/forest_basedmodel.csv", "wb"))
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))