import shutil
import base64
import json
import sys, os
from random import shuffle

#count number of files within the folder
#shuffle and pick 20% of each set randomly
TESTING_RATIO = 0.8

def countfolder(path, filetype):
    males = []
    females = []
    count_m = 0
    count_f = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((filetype)):
                if("0" in root):
                    count_m += 1
                    males.append(name)
                elif("1" in root):
                    count_f += 1
                    females.append(name)
    print("# male: ", count_m, " # female: ", count_f, )
    shuffle(males)
    shuffle(females)
    testing_m = int(count_m*TESTING_RATIO)
    testing_f = int(count_f*TESTING_RATIO)
    testing_mlist = males[testing_m:]
    testing_flist = females[testing_f:]
    training_mlist = males[:testing_m]
    training_flist = females[:testing_f]
    print(len(testing_mlist), len(training_mlist))
    print(len(testing_flist), len(training_flist))

    for i in testing_mlist:
        shutil.copy("./dataset/0/"+i, "./fdataset/valid/0/"+i)
    for i in training_mlist:
        shutil.copy("./dataset/0/"+i, "./fdataset/train/0/"+i)
    for i in testing_flist:
        shutil.copy("./dataset/1/"+i, "./fdataset/valid/1/"+i)
    for i in training_flist:
        shutil.copy("./dataset/1/"+i, "./fdataset/train/1/"+i)

    return 0

def main():
    filepath = "./dataset"
    countfolder(filepath, ".jpg")
    print("fin")

main()