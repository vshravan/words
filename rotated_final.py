# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 15:32:49 2022

@author: shari
"""

import cv2
import glob
import random
from scipy.ndimage import interpolation as inter
import os
from pathlib import Path
import pandas as pd

 
cv_img = []
path = "D:/AIML_spectrum/project2/HWD/words/a01/a01-000u" #input image path
path_rotated="D:/AIML_spectrum/project2/HWD/words_rotated/a01/a01-000u" # path to save rotated image
#path_rotated="D:/AIML_spectrum/project2/HWD/words_rotated"

file_path="D:/AIML_spectrum/project2/HWD/ascii/"  # to read updated file result.txt

df_words=pd.read_table(file_path+"result.txt",header=None)



# def create_list():
#     df_list=[]
#     df_result=pd.DataFrame()        
#     with open(file_path+"result.txt","r") as file:
#             Words= []
#             for line in file:
#                         line_split=line.split('-')
#                         text_id=line_split[0]+'-'+line_split[1]+'-'+line_split[2]+'-'+line_split[3]
#                         text=line_split[-1]
#                         df_list.append([text_id,text])
#     return df_list

def rotate_image(image , img_path) :
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    
    allowed_values = list(range(-8,9,1))
    remove=[-3,-2,-1,0,1,2,3]
    for n in remove:
        allowed_values.remove(n)
    
    # can be anything in {-5, ..., 5} \ {0}:
   #angle = random.choice(allowed_values)  
        
    angle=random.randint(-3,3)
    if angle > 0 :
        file_name_ext = "-r"+str(angle)+"p.png"
    else:
        file_name_ext = "-r"+str(abs(angle))+"n.png"
    img_rotated = inter.rotate(image, angle, reshape=False, order=0) # rotate array for given angle
    
    rotated_img_name = img_path + file_name_ext
    
    # cv2.imshow(rotated_img_name,img_rotated)
    # cv2.waitKey(0)
    cv2.imwrite(path_rotated+"\\"+rotated_img_name,img_rotated) #save rotated image
    return rotated_img_name
 

def create_img():
    Path(path_rotated).mkdir(parents=True, exist_ok=True)    
    text_list=[]
    for img in glob.glob(path +"/*.png"):
        image= cv2.imread(img)
        
        #get image file name part..
        img_name =img.replace(path,'')
        img_name =img_name.replace(".png",'')
        img_name =img_name.replace("\\",'')
        rotated_image_name=rotate_image(image , img_name)
        
        
        loc_sub =df_words[df_words[0].str.contains(img_name)]
        if not(loc_sub.empty):
            text=loc_sub.iloc[0][0].replace(img_name,'')
            text=text.replace('-','')
            text_id=rotated_image_name.replace(".png",'')
            text_updated=text_id+'-'+text
            text_list.append(text_updated)
            
    return text_list
        



final_list=create_img()

textfile=open("file_rotated.txt","w")
for element in final_list:
    textfile.write(element+"\n")
textfile.close()

