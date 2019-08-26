#ref: https://blog.csdn.net/qq_26499769/article/details/52057556

import cv2
from aip_detection import *
import matplotlib as plt
import numpy as np
import pandas as pd
import csv
from numpy import genfromtxt


def Laplacian_val(imgPath):
    '''
    ref: https://www.jianshu.com/p/b0fa7a8eba78
    '''
    img = cv2.imread(imgPath, 0)
    laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian

def brenner_val(imgPath):
    '''
    ref: https://blog.csdn.net/u013256018/article/details/86506009
    '''
    pass
    

def printHist(d):
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=d, bins='auto', color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('My Very Own Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

def writetoCsv(d1, d2):
    '''
    @param: d - 1d array of infos
    save the laplacian value to disk
    '''
    with open("laplacian_face_dataset.csv","w") as f:
        wr = csv.writer(f,delimiter="\n")
        wr.writerow(d)


def readCSV(d):
    '''
    @param: d - the csv's directory
    read the directory as sanity check
    '''
    my_data = genfromtxt(d, delimiter=',')
    print(my_data.shape)



def main():
    imgPath = "test1.jpg"
    folderpath = "./Face"
    filetype = ".jpg"
    filedir,filename = browsefolder(folderpath, filetype)
    # print(len(filedir))
    # laps = [ Laplacian_val(path) for path in filedir ]
    # print(len(laps))
    # writetoCsv(laps)
    # writetoCsv(filedir)

    # printHist(laps)
    

    # print(getImageVar(imgPath))

    # # plot images...
    # cv2.imshow("image", image)
    # cv2.waitKey(0)


    readCSV("laplacian_face_dataset.csv")
    print("fin.")


main()

