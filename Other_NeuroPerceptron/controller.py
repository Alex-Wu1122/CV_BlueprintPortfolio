import math
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from UI import Ui_Window

class Node:
    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.w = np.random.randn(dim)
        self.y = 0
    def activation_function(self, x: np.ndarray) -> None:
        v = np.dot(x, self.w)
        self.y = 1 / (1 + math.exp(-v))

    def update_w(self, η: float, curr_x: np.ndarray, error: float = None) -> None:
        self.w += η * error * curr_x

class Perceptron:
    def __init__(self, η: float, dim: int, dim_num: list) -> None:
        self.η = η
        self.dim = dim
        self.layer_list = [[Node(0) for i in range(self.dim)]]
        for i in range(1, len(dim_num)):
            self.layer_list.append([Node(dim_num[i - 1] + 1) for k in range(dim_num[i])])
    def forward_propag(self, inputs: np.ndarray, outputs: int) -> None:
        curr_x = [-1]
        for i in range(len(inputs)):
            self.layer_list[0][i].y = inputs[i]
            curr_x.append(self.layer_list[0][i].y)
        for i in range(1, len(self.layer_list)):
            next_x = [-1]
            for j in range(len(self.layer_list[i])):
                self.layer_list[i][j].activation_function(np.array(curr_x))
                next_x.append(self.layer_list[i][j].y)
            curr_x = next_x.copy()
            next_x.clear()
        if round(self.layer_list[-1][0].y) == outputs:
            err = 0
        else:
            err = outputs - self.layer_list[-1][0].y
        curr_x=np.array([-1] + [node.y for node in self.layer_list[-2]])
        self.layer_list[-1][0].update_w(self.η , curr_x, err)
        
    def predict_result(self, inputs: np.ndarray, outputs: list) -> str:
        if inputs.size == 0:
            return 'Please select data set'
        correct = 0
        for i in range(len(inputs)):       
            self.forward_propag(inputs[i],outputs[i])
            if round(self.layer_list[-1][0].y) == outputs[i]:
                correct += 1
        result=round(correct / len(inputs) * 100, 3)

        return str(result) + "%"

class WindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Window()
        self.ui.setupUi(self)
        self.button_action()
        self.data = []
        self.dim = 0
        self.cat = {}

    def button_action(self):
        self.ui.data_btn.clicked.connect(self.select_data)
        self.ui.train_btn.clicked.connect(self.training_and_show)

    def select_data(self):
        filename, filetype = QFileDialog.getOpenFileName(self, '選擇資料集', './', '文字文件 (*.txt)')
        self.ui.path_lbl.setText('-')
        self.ui.train_result.setText('-')
        self.ui.test_result.setText('-')
        self.ui.weight_result.setText('-')
        self.ui.warning_result.setText('-')
        if filename == '':
            self.ui.train_btn.setEnabled(False)
            return
        with open(filename, 'r') as file:
            self.ui.path_lbl.setText(filename.split('/')[-1])
            line = file.readline().split()
            self.dim = len(line) - 1
            self.data = np.array([[float(i) for i in line]])
            for line in file:
                self.data = np.append(self.data, [[float(i) for i in line.split()]], axis=0)
        self.cat = {}
        for i in self.data[:, -1]:
            if i not in self.cat.keys():
                self.cat[i] = len(self.cat)
        if (self.dim!=2):
            self.ui.warning_result.setText('Please select 2-dim data set!!!')
            self.ui.train_btn.setEnabled(False)
        else:
            self.ui.train_btn.setEnabled(True)

    def training_and_show(self):
        self.ui.train_btn.setEnabled(False)
        dim_num = [self.dim] + [1]
        perceptron = Perceptron(self.ui.rate_box.value(), self.dim, dim_num)
        ratio = int(len(self.data) * self.ui.ratio_box.value())
        np.random.shuffle(self.data)
        train_data = self.data[:ratio, :]
        test_data = self.data[ratio:, :]
        epoch = self.ui.epoch_box.value()
        for i in range(epoch):
            for d in train_data:
                perceptron.forward_propag(d[:-1],self.cat[d[-1]])
        self.ui.train_result.setText(
            perceptron.predict_result(train_data[:, :-1], list(map(self.cat.get, train_data[:, -1]))))
        self.ui.test_result.setText(
            perceptron.predict_result(test_data[:, :-1], list(map(self.cat.get, test_data[:, -1]))))
        
        final_weight=[]
        final_weight.append(perceptron.layer_list[-1][0].w.copy())
        self.ui.weight_result.setText(np.array2string(final_weight[0], precision=3))

        color = np.array(self.data[:, -1]).astype(int).astype(str)
        symbol=[]
        for d in self.data:
            if np.any(np.all(d == train_data, axis=1)):
                symbol.append('train')
            else:
                symbol.append('test')
        fig = px.scatter(x=self.data[:, 0], y=self.data[:, 1], color=color, symbol=symbol)
        x = np.array([np.min(self.data[:, 0]) , np.max(self.data[:, 0]) ])
        y = (final_weight[0][0] - x * final_weight[0][1]) / final_weight[0][2]
        fig.add_trace(go.Scatter(x=x, y=y, name='train_result'))
        fig.show()
        self.ui.train_btn.setEnabled(True)
