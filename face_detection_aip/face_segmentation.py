
'''
how to use:
    >> python3  face_seg.py   folder_path     output_folder_path    ( file_type  image_size)
    >> python3  face_seg.py   ./test_folder   ./test_outputfolder   ( .jpg       64        )
dependencies: 
    >> pip3 install aip

connect with baidu ai 
1. save the info as .json file 
2. chop the image and save the detected faces ((max face num in an image: 10; image size: 64)
July 1, 2019
'''


from aip_detection import *
import cv2
from torchvision.transforms import Compose, ToTensor, Normalize, Resize

def main():
    img_size = 64
    file_type = ".jpg" 
    outputfile_dir = "./test_outputfolder/" 

    #for a directory
    folder_path = "./test_folder" 
    file_dirs, file_names = browsefolder(folder_path,file_type)

    #take command line arguments
    arglist = sys.argv
    if(len(arglist) > 1):
        folder_path = str(sys.argv[1])
    if(len(arglist) > 2):
        outputfile_dir = str(sys.argv[2]) + "/"
    if(len(arglist) > 3):
        file_type = str(sys.argv[3])
    if(len(arglist) > 4):
        img_size = str(sys.argv[4])


    count = 0
    for file_dir in file_dirs:
        img = cv2.imread(file_dir)
        
        #getting the location using baidu.ai #ref: http://ai.baidu.com/
        json_data = connectwithbaiduai(file_dir)

        try:
            #save all the info as json
            saveas_json(json_data,outputfile_dir+file_names[count])
            #retrieve only the location info
            locations = recog_location(json_data)
        except KeyError:
            json_data = connectwithbaiduai(file_dir)
            print("key_error!")
            pass

        num_of_faces = len(locations)
        for i in range(num_of_faces):
            #retrieve location info to indicate where to chop
            left = int(locations[i]['left'])
            top = int(locations[i]['top'])
            width = int(locations[i]['width'])
            height = int(locations[i]['height'])

            #chop and resize image using opencv
            crop_img = img[ top:top+height,left:left+width]
            resized_chop_img = cv2.resize(crop_img,(img_size,img_size))

            #write to disk
            outputfile_name = outputfile_dir+file_names[count]+"_"+str(i+1)+file_type
            status = cv2.imwrite(outputfile_name, resized_chop_img)

        count += 1
        if(count % 10 == 0):
            print(count)

    print("fin")

main()