from aip_detection import *
import json


def findDuplicated(lines):
  out = []
  for line in lines:
    info = line.split(",")
    if("na" in info[0]):
      temp_name = info[0][:-8]
      out.append(temp_name)
  return out


def rmDuplicated(lines, du):
    # for line in lines:
    #   if()
    pass

def rmNa(lines):
    pass

def main():
    file_type = ".json"
    folder_path = "./Face/2019_6_1/2"
    output_filename = "gender_labels_2.txt"
    arglist = sys.argv
    if(len(arglist) > 1):
        folder_path = str(sys.argv[1])
    if(len(arglist) > 2):
        output_filename = str(sys.argv[2])


    text_file = open(folder_path, "r")
    lines = text_file.read().split('\n')

    du = findDuplicated(lines)
    print(du)
    # files,genders = rmDuplicated(lines, du)

    # #write to a file  - errors log
    # with open(output_filename, "w") as f:
    #     for filename, gender in zip(files, genders):
    #         f.write(filename+","+str(gender)+"\n")
    # f.close()

    # print(set(genders))
    # print(len(files), len(genders))
    print("fin.")

main()