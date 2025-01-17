# -*- coding: utf-8 -*-

'''
LabelMe JSON format -> YOLO txt format
save dataset (학습 자료) in dataset/ 
output will be saved in result/
JSON format will be moved to json_backup/

Finally, please manually copy text file together with image into 1 folder. (Easier to maintain)
마지막으로 txt파일이랑 이미지파일이랑 같은 폴더에 복사하세요 (관리하기 위한 쉬움)
'''

import os
from os import walk, getcwd
import json

from PIL import Image

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = "./dataset/"
outpath = "./result/"
json_backup ="./json_backup/"

wd = getcwd()
#list_file = open('%s_list.txt'%(wd), 'w')

""" Get input json file list """
json_name_list = []
for file in os.listdir(mypath):
    if file.endswith(".json"):
        json_name_list.append(file)

""" Process """
for json_name in json_name_list:
    json_path = mypath + json_name
    print("Input:" + json_path)
    json_data = json.load(open(json_path, 'r'))
    
    """ Open output text files """
    txt_name = json_name.rstrip(".json") + ".txt"
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a")

    """ Convert the data to YOLO format """ 
    for shape in json_data['shapes']:

        points = shape['points']
        x1 = float(points[0][0])
        y1 = float(points[0][1])
        x2 = float(points[1][0])
        y2 = float(points[1][1])

        label = shape['label']

        #in case when labelling, points are not in the right order
        xmin = min(x1,x2)
        xmax = max(x1,x2)
        ymin = min(y1,y2)
        ymax = max(y1,y2)
        img_path = str('%s/dataset/%s.png'%(wd, os.path.splitext(json_name)[0]))

        im = Image.open(img_path)
        w = int(im.size[0])
        h = int(im.size[1])

        print(w, h)
        print(xmin, xmax, ymin, ymax)
        b = (xmin, xmax, ymin, ymax)
        bb = convert((w,h), b)
        print(bb)
        txt_outfile.write(label + " " + " ".join([str(a) for a in bb]) + '\n')