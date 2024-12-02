import os 
import shutil
import csv

def Dcm2jpg(file_path):
	f1 = []
	num = 1
	error = 0

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

			for file3 in f3:
				try:#首先偵錯，去除找路徑時會出錯的圖片
					if os.path.exists(file_path+'/'+file1+'/'+file2+'/'+file3+'.jpg'):
						orig = file_path+'/'+file1+'/'+file2+'/'+file3+'.jpg' #圖片位置
						path = './four_target/'#分類後的dst資料夾

						with open("train_study_level.csv", 'r') as file:
							folder = file1 + "_study"#圖片的dst位置
							csvreader = csv.reader(file)

							for row in csvreader:#查看圖片為四類中的哪一類，並複製一份到相應的資料夾裡(NEP,TA,IA,AA)
								if row[0] == folder:
									if row[1] == '1':
										shutil.copyfile(orig, path + 'NFP/' + folder + '.jpg')
										print('succed', num)
										num += 1
									elif row[2] == '1':
										shutil.copyfile(orig, path + 'TA/' + folder + '.jpg')
										print('succed', num)
										num += 1
									elif row[3] == '1':
										shutil.copyfile(orig, path + 'IA/' + folder + '.jpg')
										print('succed', num)
										num += 1
									elif row[4] == '1':
										shutil.copyfile(orig, path + 'AA/' + folder + '.jpg')
										print('succed', num)
										num += 1
									else:#有時部分檔案會出錯
										error += 1
										print('target not found!')
					else:
						 print(file3, "file not found!")
				except:
					pass

	print(error)

Dcm2jpg('./pictchange')
