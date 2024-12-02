import pydicom
import matplotlib.pyplot as plt
import scipy.misc
import pandas as pd 
import numpy as np
import os 
import cv2
import imageio
from PIL import Image
from scipy import misc
import imageio
import matplotlib.pyplot as plt

def Dcm2jpg(file_path):
    f1 = []
    
    names = os.listdir(file_path)#指向第一層裡的所有資料夾
    for name in names:
        f1.append(name)

    for file1 in f1:
        f2 = []
        names = os.listdir(file_path+'/'+file1)#指向第二層裡的所有資料夾
        for name in names:
            f2.append(name)
        for file2 in f2:
            f3 = []
            names = os.listdir(file_path+'/'+file1+'/'+file2)#指向第三層裡的所有圖片
            for name in names:
                index = name.rfind('.')
                name = name[:index]#只留檔名
                f3.append(name)
            print(f3)
            for file3 in f3:
                print('C:/Users/User/Desktop/pict/'+file1+'/'+file2+'/'+file3)
                if os.path.exists('C:/Users/User/Desktop/pict/'+file1):#查看out_path是否存在
                    pass
                else:
                    os.makedirs('C:/Users/User/Desktop/pict/'+file1)#不存在就創一個

                if os.path.exists('C:/Users/User/Desktop/pict/'+file1+'/'+file2):#查看out_path是否存在
                    pass
                else:
                    os.makedirs('C:/Users/User/Desktop/pict/'+file1+'/'+file2)#不存在就創一個

                try:#首先偵錯，去除找路徑時會出錯的圖片
                    if os.path.exists(file_path+'/'+file1+'/'+file2+'/'+file3+'.dcm'):
                        picture_path = file_path+'/'+file1+'/'+file2+'/'+file3+'.dcm'#原先下載下來的檔案是.dcm
                        out_path = 'C:/Users/User/Desktop/pict/'+file1+'/'+file2+'/'+file3+'.jpg'

                        ds = pydicom.read_file(picture_path)
                        img = ds.pixel_array#將dcm裡的圖片資料取出
                        
                        img.dtype = "int16"#原本為int8，會導致圖片嚴重扭曲
                        imageio.imwrite(out_path,img)#把JPG存到目的地資料夾
                        
                    else:
                        pass
                except:
                    pass
                
        
Dcm2jpg('D:/Kaggle')

