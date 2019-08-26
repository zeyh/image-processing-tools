'''
some helper functions to connect with baidu ai and retrive specific data info
June 25, 2019
'''
from aip import AipFace
import base64
import json
import sys, os, time

def connectwithbaiduai(file_path):
    '''
    @param: file_path: a string of the image's file name
    @return: a string indicating the image's gender
    connect with baidu ai and get the json data
    ref: https://www.cnblogs.com/dmass36/p/10182183.html
    '''
    #百度接口信息
    APP_ID = '16617513'       
    API_KEY = 'ZfZGzKTMMdC82ZkmZKMevvG3'       
    SECRET_KEY = 'PKpDDoLBIfNjLUAoSaQBT5cXpv5qqlIL'   
    client = AipFace(APP_ID,API_KEY,SECRET_KEY)
    imageType = "BASE64"

    #定义参数变量
    options = {}
    options["max_face_num"] = 10
    options["face_field"] = "gender"

    # 初始化AirFace对象
    aipface = AipFace(APP_ID, API_KEY, SECRET_KEY)

    #打开文件
    with open(file_path, 'rb') as fp:
        # infile = fp.read()
        base64_date = base64.b64encode(fp.read())
        image = str(base64_date,encoding='utf-8')
        result = client.detect(image, imageType, options)

    #将百度接口返回的数据转成json对象
    json_str = json.dumps(result)

    #对数据进行解码
    json_data = json.loads(json_str)

    return json_data




def recog_location(json_data):
    '''
    @param: json_data: json data contains the info of an given image generated from baidu ai
    @return: a list of json location infos
    get the location info based on the json_data input
    '''
    num_of_faces = len(json_data['result']['face_list'])
    locations = [json_data['result']['face_list'][face]['location']  for face in range(num_of_faces) ]
    
    return locations


def recog_gender(file_dir,filename,count):
    '''
    @param: json_data: json data contains the info of an given image generated from baidu ai
    @return: gender info for an image containing only 1 face
    get the first gender info based on the json_data input
    '''
    json_data = connectwithbaiduai(file_dir)
    
    try:
        gender = json_data['result']['face_list'][0]['gender']['type']
    except (TypeError, ValueError, KeyError) as error:
        if(count < 11):
            gender = recog_gender(file_dir,filename, count+1)
        if(json_data['error_code'] == 222202):
            return "na"
        if(json_data['error_code'] == 18):
            return "qps"
        else:
            print("-1", json_data)
            return "-1"
        # print("key error!")
    return gender


def saveas_json(file_dir, outputfile_name,count):
    '''
    @param: json_data: json data contains the info of an given image generated from baidu ai
    @param: outputfile_name: the directory you want to save the json file to (eg: ./test_outputfolder/) 
    save the json data to the disk as .json file
    '''
    json_data = connectwithbaiduai(file_dir)
    time.sleep(0.3)
    try:
        # print(outputfile_name+'.json')
        with open(outputfile_name+'.json', 'w') as outfile:  
            json.dump(json_data, outfile)
        outfile.close()
    except (TypeError, ValueError, KeyError) as error:
        pass




def browsefolder(path, filetype):
    '''
    @param: path: string of folder name, 
    @param: filetype: string of file type
    @return: a list of all qualified filename
    traverse the all the files satisfy the type within a given folder
    ref: https://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
    '''
    filedirs = []
    filenames = []
    count = 0
    max_count = 10
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith((filetype)):
                filedirs.append(root+"/"+name)    
                name_temp = name.replace(filetype,"")
                root_temp = root.replace("./", "")
                filenames.append(name_temp)
                count += 1
                # if(count > max_count):
                #     break
    return filedirs, filenames

