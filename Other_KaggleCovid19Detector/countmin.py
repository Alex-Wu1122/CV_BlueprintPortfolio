import pydicom # 用來解析dicom格式圖像的向素值
import numpy as np
import cv2 # 用於保存圖片
import os

def Dcm2jpg(file_path):
    f = []
    mi=9000000000
    names = os.listdir(file_path)#指向存放所有JPG的資料夾
    for name in names:
        index = name.rfind('.')#去除副檔名
        name = name[:index]
        f.append(name)
    for files in f:
        picture_path = "C:/Users/User/Desktop/folder_jpg/"+files+".jpg"#拼接成完整的路徑
        try:#使用try避免在找路徑時出錯
            if os.path.exists(picture_path):
                img = cv2.imread(picture_path)
                sp = img.shape
                x = sp[0]*sp[1]
                if x<mi:#將最小的圖片資訊記下來，以供之後裁切參考
                    finally1=sp[1]
                    finally0=sp[0]
                    mi=x
                    result=files
        except:
            pass
    print(finally0)
    print(finally1)
    print(mi)
    print(result)        

Dcm2jpg('C:/Users/User/Desktop/folder_jpg')
