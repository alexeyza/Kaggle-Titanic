import csv as csv 
import numpy as np

def main():
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

    print survival_table

if __name__ == '__main__':
    main()