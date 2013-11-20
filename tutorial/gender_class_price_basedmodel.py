import csv as csv 
import numpy as np

def create_model(survival_table):
    test_file_obect = csv.reader(open('../csv/test.csv', 'rb'))
    header = test_file_obect.next()

    predictions_file = csv.writer(open("../csv/gender_class_price_basedmodelpy.csv", "wb"))
    predictions_file.writerow(["PassengerId", "Survived"])

    fare_ceiling = 40
    fare_bracket_size = 10
    number_of_price_brackets = fare_ceiling / fare_bracket_size
    number_of_classes = 3

    for row in test_file_obect:
        for j in xrange(number_of_price_brackets):
            try:
                row[8] = float(row[8])
            except:
                bin_fare = number_of_classes-float(row[1])
                break
            if row[8] > fare_ceiling:
                bin_fare = number_of_price_brackets-1
                break
            if row[8] >= j*fare_bracket_size and row[8] < (j+1)*fare_bracket_size:
                bin_fare = j
                break
        if row[3] == 'female':
            predictions_file.writerow([row[0], int(survival_table[0,float(row[1])-1,bin_fare])])
        else:
            predictions_file.writerow([row[0], int(survival_table[1,float(row[1])-1,bin_fare])])

def train():
    csv_file_object = csv.reader(open('../csv/train.csv', 'rb')) 
    header = csv_file_object.next()

    data=[]
    for row in csv_file_object:
        data.append(row)
    data = np.array(data)

    fare_ceiling = 40
    data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling-1.0
    fare_bracket_size = 10
    number_of_price_brackets = fare_ceiling / fare_bracket_size
    number_of_classes = 3

    survival_table = np.zeros((2, number_of_classes, number_of_price_brackets))

    for i in xrange(number_of_classes):
        for j in xrange(number_of_price_brackets):
            women_only_stats = data[
            (data[0::,4] == "female")
            &(data[0::,2].astype(np.float) == i+1)
            &(data[0:,9].astype(np.float) >= j*fare_bracket_size)
            &(data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]

            men_only_stats = data[
            (data[0::,4] != "female")
            &(data[0::,2].astype(np.float) == i+1)
            &(data[0:,9].astype(np.float) >= j*fare_bracket_size)
            &(data[0:,9].astype(np.float) < (j+1)*fare_bracket_size), 1]

            survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
            survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

    survival_table[ np.isnan(survival_table) ] = 0.

    survival_table[ survival_table < 0.5 ] = 0
    survival_table[ survival_table >= 0.5 ] = 1 

    return survival_table

def main():
    create_model(train())

if __name__ == '__main__':
    main()