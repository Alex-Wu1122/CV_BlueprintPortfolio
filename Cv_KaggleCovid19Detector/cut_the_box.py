import cv2
import os
import pandas as pd 
import os 
import cv2
import re
df = pd.read_csv(r'C:\Users\User\Desktop\visual code\python\資科\train_image_level.csv')
def Dcm2jpg(file_path):
    count = 1
    f1 = []
    names = os.listdir(file_path)
    for name in names:
        f1.append(name)
    for file1 in f1:
        f2 = []
        names = os.listdir(file_path+'/'+file1)
        for name in names:
            f2.append(name)
        for file2 in f2:
            f3 = []
            names = os.listdir(file_path+'/'+file1+'/'+file2)
            for name in names:
                index = name.rfind('.')
                name = name[:index]
                f3.append(name)
            for file3 in f3:
                print(count)
                count+=1
                print(file3)
                for i in range(len(df['boxes'])):
                    if (file3 == df['id'][i][:-6] and not(df['boxes'][i]!=df['boxes'][i])):
                        str = df['boxes'][i]
                        position = re.findall(r"\d+\.?\d*",str)
                        x1 = int(float(position[0]))
                        y1 = int(float(position[1]))
                        w1 = int(float(position[2]))
                        h1 = int(float(position[3]))
                        if(len(position)>4):
                            x2 = int(float(position[4]))
                            y2 = int(float(position[5]))
                            w2 = int(float(position[6]))
                            h2 = int(float(position[7]))
                if os.path.exists('C:/Users/User/Desktop/pict/'+file1):
                    pass
                else:
                    os.makedirs('C:/Users/User/Desktop/pict/'+file1)

                if os.path.exists('C:/Users/User/Desktop/pict/'+file1+'/'+file2):
                    pass
                else:
                    os.makedirs('C:/Users/User/Desktop/pict/'+file1+'/'+file2)

                try:
                    if os.path.exists(file_path+'/'+file1+'/'+file2+'/'+file3+'.jpg'):
                        src = cv2.imread(file_path+'/'+file1+'/'+file2+'/'+file3+'.jpg')
                        left = src[y1:y1+h1,x1:x1+w1]
                        right = src[y2:y2+h2,x2:x2+w2]
                        cv2.imwrite('C:/Users/User/Desktop/pict/'+file1+'/'+file2+'/'+file3+'_left'+'.jpg',left)
                        cv2.imwrite('C:/Users/User/Desktop/pict/'+file1+'/'+file2+'/'+file3+'_right'+'.jpg',right)
                    else:
                        pass
                except:
                    pass 
Dcm2jpg('D:/pictchange')
    

