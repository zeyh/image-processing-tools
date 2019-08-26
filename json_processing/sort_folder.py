#extract only the faces that can be detected
#read the label file, if 0 or 1, copy to another folder

from aip_detection import *
import shutil
import base64
import json
import sys, os


def readlabels(filepath, dstpath):
    text_file = open(filepath, "r")
    lines = text_file.read().split('\n')
    for line in lines:
        line_list = line.split(",")
        if(len(line_list) == 2):
            if(line_list[1] == "0"):
                file_name = line_list[0].split("/")[-1]
                # print(file_name)
                shutil.copy(line_list[0], dstpath+"0/")
            elif(line_list[1] == "1"):
                file_name = line_list[0].split("/")[-1]
                # print(file_name)
                shutil.copy(line_list[0], dstpath+"1/")
    pass

def main():
    labelfile_path = "gender_labels.txt"
    dst_path = "./dataset/"
    readlabels(labelfile_path, dst_path)




    print("fin")

main()


