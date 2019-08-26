
'''
full dataset size: 96093
July 1, 2019
'''

from aip_detection import *


def main():
    file_type = ".jpg" 

    #for a directory
    folder_path = "error_log_18.txt" 

    arglist = sys.argv
    if(len(arglist) > 1):
        folder_path = str(sys.argv[1])

    text_file = open(folder_path, "r")
    lines = text_file.read().split('\n')

    print(len(lines))

    count = 0
    for file_dir in lines:
        #getting the location using baidu.ai #ref: http://ai.baidu.com/
        # json_data = connectwithbaiduai(file_dir)
        try:
            file_name = file_dir.replace(file_type,"")

            saveas_json(file_dir, file_name,1)
            count += 1
            if(count % 50 == 0):
                print(count, file_dir)


        except (TypeError, ValueError, KeyError) as error:
            pass


    print("fin")

main()