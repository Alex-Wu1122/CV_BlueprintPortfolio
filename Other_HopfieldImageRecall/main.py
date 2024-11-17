import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog

from UI import Ui_MainWindow




class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Project3')
        self.ui.graph_box.setEnabled(False) #還未選取資料集，故設False
        self.ui.train_btn.setEnabled(False) #還未選取資料集，故設False
        self.epoch = 1
        self.b = 0 #底
        self.h = 0 #高
        self.size = 0 #圖片大小
        self.train_path = '' #訓練資料路徑
        self.test_path = '' #測試資料路徑
        self.training_data = None #訓練資料
        self.testing_data = None #測試資料
        self.ui.train_btn.clicked.connect(self.Train) #觸發訓練事件的按鈕
        self.ui.choose_box.currentIndexChanged.connect(self.choose_box) #選擇資料集
        self.ui.graph_box.currentIndexChanged.connect(self.change_graph) #選擇第幾張圖片
        self.ui.epoch_box.valueChanged.connect(self.change_epoch) #選擇epoch

    def Train(self):
        #####清空圖片選擇欄以及三個圖片區塊####
        self.ui.graph_box.setEnabled(True)
        self.ui.graph_box.clear()
        self.ui.train_table.clearContents()
        self.ui.test_table.clearContents()
        self.ui.test_recall_table.clearContents()


        #####取得資料集####
        self.training_data = self.read_file(self.train_path)
        self.testing_data = self.read_file(self.test_path)


        ####依照資料集裡的圖片數新增欄位####
        for i in range(self.training_data.shape[0]):
            self.ui.graph_box.addItem("Graph "+str(i+1))

        self.recall = [] #初始化回想結果的矩陣
        w_matrix = np.zeros((self.size, self.size))#創立權重矩陣

        #####curr_graph為已經扁平化的圖片陣列，依照公式，矩陣相乘後，累加到權重矩陣####
        for curr_graph in self.training_data:
            w_matrix = np.add(w_matrix,curr_graph.T @ curr_graph)

        for i in range(self.size):
            w_matrix[i][i] = 0 #斜的那排要為0
        θ = w_matrix.sum(axis=0).reshape((-1, 1)) #每一行相加合併後，再轉換成列，求得θ


        for curr_graph in self.testing_data:
            x = np.array(curr_graph).copy().T
            for e in range(self.epoch): 
                y = w_matrix @ x - θ #依照公式求得預測值
                for i in range(self.size):#判斷是否通過激活函數
                    if y[i] == 0:
                        y[i] = x[i]
                    elif y[i] > 0:
                        y[i] = 1 
                    else:
                        y[i] = -1
                x = y.copy()
            self.recall.append(x.copy().T)#將預測結果增加到recall
        
        
    def choose_box(self,index):
        if index==0:#選擇Basic
            self.train_path='./Basic_Training.txt'
            self.test_path='./Basic_Testing.txt'
            
        else:#選擇Bonus
            self.train_path='./Bonus_Training.txt'
            self.test_path='./Bonus_Testing.txt'
        self.ui.train_btn.setEnabled(True)
        self.ui.graph_box.setEnabled(False)

    def change_graph(self,index):

        ###創建黑色與白色兩個區塊###
        Black = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        Black.setStyle(QtCore.Qt.SolidPattern)
        White = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        White.setStyle(QtCore.Qt.SolidPattern)
        
        ###將一行的圖片陣列轉換成圖片矩陣並開始填入表格顏色
        graph = self.training_data[index].reshape((self.h, self.b))
        for i in range(self.h):
            for j in range(self.b):
                Table_Item = QtWidgets.QTableWidgetItem()
                if graph[i][j] == 1:
                    Table_Item.setBackground(Black)
                else:
                    Table_Item.setBackground(White)
                self.ui.train_table.setItem(i, j, Table_Item)
        
        graph = self.testing_data[index].reshape((self.h, self.b))
        for i in range(self.h):
            for j in range(self.b):
                Table_Item = QtWidgets.QTableWidgetItem()
                if graph[i][j] == 1:
                    Table_Item.setBackground(Black)
                else:
                    Table_Item.setBackground(White)
                self.ui.test_table.setItem(i, j, Table_Item)
        
        graph = self.recall[index].reshape((self.h, self.b))
        for i in range(self.h):
            for j in range(self.b):
                Table_Item = QtWidgets.QTableWidgetItem()
                if graph[i][j] == 1:
                    Table_Item.setBackground(Black)
                else:
                    Table_Item.setBackground(White)
                self.ui.test_recall_table.setItem(i, j, Table_Item)

    def change_epoch(self,index):
        self.epoch=index #取得epoch
        #清空圖片選擇欄以及三個圖片區
        self.ui.graph_box.clear()
        self.ui.graph_box.setEnabled(False)
        self.ui.train_table.clearContents()
        self.ui.test_table.clearContents()
        self.ui.test_recall_table.clearContents()
   
    def map_values(i):
        return 1 if i == '1' else -1
    def read_file(self, path: str) -> list:
        self.h = 0
        graph_num = 1
        data = np.array([])
        with open(path) as file:
            file = file.readlines()
        self.b = len(file[0]) - 1
        for line in file:
            if line == file[-1]:
                pass
            else:
                line = line[:-1]
            if line == '':
                graph_num += 1
                continue
            if graph_num == 1:
                self.h += 1
            list_append=[]
            for i in list(line):
                if i =='1':
                    list_append.append(1)
                else:
                    list_append.append(-1)
            data = np.append(data, list_append)
        self.size = self.h * self.b
        data_list=data.reshape((graph_num, 1, self.size)) 
        return data_list


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec_())
