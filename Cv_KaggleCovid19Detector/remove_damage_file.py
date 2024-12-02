import os 
import shutil
import cv2
import numpy as np

orig_path = ['./four_target/NFP/', './four_target/IA/', './four_target/AA/', './four_target/TA/']
#已將圖片分類為四類，並分別放置於相對應的資料夾
p = ['NFP', 'IA', 'AA', 'TA']
n = []
c = []
t = []

for path in orig_path:
	num = 1
	cnt = 1
	names = os.listdir(path)

	for name in names:
		try:#檢查圖片是否能成功讀取
			img = cv2.imread(path + '/' + name)
			cv2.imshow('hi', img)
			num += 1

		except:#無法讀取的圖片就刪除掉
			os.remove(path + name)
			print(path, "Removed!", cnt)
			cnt += 1

	n.append(num)#該分類圖片的成功數量
	c.append(cnt)#該分類圖片的失敗數量
	t.append(len(names))#該分類圖片的總數量


for i in range(4):#將四個分類的成功數,失敗數,總數依依展示
	print("path:", p[i])
	print("succeed", n[i])
	print("failed", c[i])
	print("total", t[i])
