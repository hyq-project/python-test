import csv


def read_csv(file):
    count_num = 80
    list1 = []
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            count_num -= 1
            list1.extend(row)
            if count_num == 0:
                print(list1)
                list1 = []
                count_num += 80