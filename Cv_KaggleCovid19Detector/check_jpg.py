import os 
import shutil
import cv2
import numpy as np

path = 'folder_jpg'#此資料夾存放了所有未分類的JPG

num = 1
cnt = 1
names = os.listdir(path)

for name in names:
	try:#判斷JPG能否正常讀取，並計算成功與失敗的數量
		img = cv2.imread(path + '/' + name)
		cv2.imshow('hi', img)
		print("successfully", num)
		num += 1

	except:
		print("failed", cnt)
		cnt += 1
print("succeed", num)#成功讀取的圖片數
print("failed", cnt)#失敗讀取的圖片數
print("total", len(names))#總圖片數
