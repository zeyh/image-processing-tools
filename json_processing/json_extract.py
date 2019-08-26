'''
full dataset size: 96093
July 12, 2019
'''
from aip_detection import *
import json

def browsefolder_json(path, filetype):
    '''
    @param: path: string of folder name, 
    @param: filetype: string of file type
    @return: a list of all qualified filename
    traverse the all the files satisfy the type within a given folder
    ref: https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
    '''
    filedirs = []
    error_codes = []
    count = 0
    max_count = 10
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((filetype)):

                filedir_temp = root+"/"+name
                json_temp = json.loads(open(filedir_temp).read())
                if (json_temp['error_code'] != 0):
                    filedirs.append(filedir_temp)    
                    error_codes.append(json_temp['error_code'])

                count += 1
                # if(count > max_count):
                #     break
    return filedirs, error_codes


def main():
    file_type = ".json"
    folder_path = "./Face/2019_6_1/2"
    output_filename = "errors_log.txt"
    arglist = sys.argv
    if(len(arglist) > 1):
        folder_path = str(sys.argv[1])
    if(len(arglist) > 2):
        output_filename = str(sys.argv[2])


    # file_dirs, file_names = browsefolder(folder_path,file_type)
    files, errors = browsefolder_json(folder_path,file_type)


    #write to a file  - errors log
    with open(output_filename, "w") as f:
        for filename, error in zip(files, errors):
            f.write(filename+","+str(error)+"\n")
    f.close()

    #write to a file  - errors log
    with open("error_log_18.txt", "w") as f:
        for filename, error in zip(files, errors):
            if(error == 18):
                filename_temp = filename.replace(file_type,".jpg")
                f.write(filename_temp+"\n")
    f.close()

    print(set(errors))
    print(len(files), len(errors))
    print("fin.")

main()