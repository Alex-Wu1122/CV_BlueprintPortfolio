import math
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle



class Neuron:
    def __init__(self, m: np.ndarray, σ: float):
        self.w = random.random()
        self.m = m
        self.σ = σ
        self.y = 0

    def φ(self, x: np.ndarray) -> None:
        self.y = math.exp(-((x - self.m) ** 2).sum() / (2 * self.σ ** 2))

    def update(self, η: float, error: float, x: np.ndarray) -> None:
        curr_w = self.w
        curr_m = self.m.copy()
        curr_σ = self.σ
        same = η * error * self.y
        self.w += same
        self.m += same * curr_w  * (x - curr_m)/( curr_σ ** 2)
        self.σ += same * curr_w  * ((x - curr_m) ** 2).sum()/(curr_σ ** 3) 




def get_x_y_dis( car_x: int, car_y: int, deg: float) -> np.ndarray:
    x_wall = [(-6, -3, 22), (6, -3, 10), (18, 22, 50), (30, 10, 50)]
    y_wall = [(-3, -6, 6), (10, 6, 30), (22, -6, 18), (50, 18, 30)]
    min_x_y_dis = []
    for i in range(3):
        min_x_y_dis.append((0,0,math.inf))
    left_front_right=[-1,0,1]
    for i in left_front_right:
        for x, l, h in x_wall:
            k = (x - car_x) / math.cos(deg + i * math.pi / 4)
            y = car_y + k * math.sin(deg + i * math.pi / 4)
            dis = math.dist((car_x,car_y), (x, y))
            if k >= 0 and l <= y <= h and dis < min_x_y_dis[i+1][2]:
                min_x_y_dis[i+1] = (x, y, dis)
        for y, l, h in y_wall:
            k = (y - car_y) / math.sin(deg + i * math.pi / 4)
            x = car_x + k * math.cos(deg + i* math.pi / 4)
            dis = math.dist((car_x,car_y), (x, y))
            if k >= 0 and l <= x <= h and dis < min_x_y_dis[i+1][2]:
                min_x_y_dis[i+1] = (x, y, dis)
    return np.array([min_x_y_dis[1], min_x_y_dis[2], min_x_y_dis[0]])


class RBFN:
    def __init__(self,file_dim: int):
        self.d = file_dim
        path = f'./train{self.d}dAll.txt'
        with open(path) as file:
            line = file.readline().split()
            self.kmeans_dist=np.array([math.inf])
            self.kmeans_who=np.array([-1])
            self.data = np.array([[float(i) for i in line]])
            for line in file:
                line = line.split()
                self.kmeans_dist = np.append(self.kmeans_dist,[math.inf], axis=0)
                self.kmeans_who = np.append(self.kmeans_who,[-1], axis=0)
                self.data = np.append(self.data, [[float(i) for i in line]], axis=0)
        with open('軌道座標點.txt') as file:
            line = file.readline().split()
            line_arr = line[0].split(',')
            car_x=int(line_arr[0])
            car_y=int(line_arr[1])
            deg = math.radians(int(line_arr[2]))

            line = file.readline().split()
            line_arr = line[0].split(',')
            self.final_line_left_x=int(line_arr[0])
            self.final_line_left_y=int(line_arr[1])
            line = file.readline().split()
            line_arr = line[0].split(',')
            self.final_line_right_x=int(line_arr[0])
            self.final_line_right_y=int(line_arr[1])
            self.final_line_width=self.final_line_right_x-self.final_line_left_x
            self.final_line_height=self.final_line_right_y-self.final_line_left_y
            self.road_x=[]
            self.road_y=[]
            for line in file:
                line_arr=line.split(',')
                self.road_x.append(int(line_arr[0]))
                self.road_y.append(int(line_arr[1]))    
        self.d -= 1
        self.neuron_group = []
        print('******第一階段非監督式學習(k-means)******')
        K=int(input('請輸入分群數量(K): '))
        self.kmeans(K)

        epoch, bias = 50, -1
        print(('******開始訓練******'))
        print("Epoch\tη\tloss\tbias")
        for e in range(epoch):
            loss = 0
            #η = 0.1* np.exp(-0.1 * e) #指數
            η = (epoch - e) / epoch * 0.1 #線性
            for data in self.data:
                predict = bias
                for neuron in self.neuron_group:
                    neuron.φ(data[:self.d])
                    predict += neuron.w * neuron.y
                for neuron in self.neuron_group:
                    neuron.update(η, data[self.d] - predict, data[:self.d])
                bias += η * (data[self.d] - predict)
                loss += (data[self.d] - predict) ** 2 / 2
            loss /= len(self.data)
            print(f'{e + 1}\t{round(η,3)}\t{round(loss,4)}\t  {round(bias,4)}')
        print()
        print(f'******類神經元的訓練結果******')
        print('Neuron \t Weight \t\t Mean \t\t\t\t\t\t standard')
        k=1
        for neuron in self.neuron_group:
            print(f'{k} \t {neuron.w} \t {neuron.m} \t\t {neuron.σ}')
            k+=1
        print('******啟動自駕車(RNFN)******')
        self.steps_group = []
        All_result = []
        self.pas = True
        self.steps_group.append([[car_x,car_y], deg, get_x_y_dis(car_x,car_y, deg)])
        while car_y < self.final_line_right_y-3:
            all_x_y_dis = get_x_y_dis(car_x,car_y, deg)
            predict = bias
            for neuron in self.neuron_group:
                if self.d==3:
                    neuron.φ(all_x_y_dis[:, 2])
                elif self.d==5:
                    neuron.φ(np.append([car_x,car_y], all_x_y_dis[:, 2]))
                predict += neuron.w * neuron.y
            predict *= -1
            if self.d==3:
                result=f'{all_x_y_dis[:, 2][0]} {all_x_y_dis[:, 2][1]} {all_x_y_dis[:, 2][2]} {predict}\n'
            elif self.d==5:
                result =f'{car_x} {car_y} {all_x_y_dis[:, 2][0]} {all_x_y_dis[:, 2][1]} {all_x_y_dis[:, 2][2]} {predict}\n' 
            All_result.append(result)
            predict = math.radians(predict)
            self.steps_group.append([[car_x,car_y], deg, all_x_y_dis])
            if car_x < -3 or car_x > 27 or car_y < 0:
                self.pas = False
                break
            elif 0<car_y<10 and (car_x>3 or car_x<-3 or math.dist((car_x,car_y), (6, 10))<3):
                self.pas = False
                break
            elif 10<car_y<22 and (car_x>27 or car_x<-3 or math.dist((car_x,car_y), (6, 10))<3 or math.dist((car_x,car_y), (18, 22))<3):
                self.pas = False
                break
            elif 22<car_y<50 and (car_x>27 or car_x<15 or math.dist((car_x,car_y), (18, 22))<3):
                self.pas = False
                break
            elif -6<car_x<6 and (car_y>19 or car_y<0):
                self.pas = False
                break
            elif 6<car_x<18 and (car_y>19 or car_y<7):
                self.pas = False
                break
            elif 18<car_x<30 and car_y<7:
                self.pas = False 
                break
            
            car_x += math.cos(deg + predict) + math.sin(predict) * math.sin(deg) #考慮到車體的旋轉
            car_y += math.sin(deg + predict) - math.sin(predict) * math.cos(deg)
            deg = (deg - math.asin(2 * math.sin(predict)/3 )) % (math.pi * 2) #決定要減緩或加速角度變化
            
        with open(f'track{self.d+1}D.txt', 'w') as file:
            file.writelines(All_result)
        fig = plt.figure(figsize=(8 ,5))
        plt.get_current_fig_manager().set_window_title('project2')
        self.sub_plot = plt.subplot2grid((1, 3), (0, 1), colspan=2)
        self.sub_plot.set_aspect('equal', 'box')
        anim=animation.FuncAnimation(fig, self.draw, frames=len(self.steps_group),repeat=False)
        plt.show()

    def kmeans(self, K) -> None:
        K_center = self.data[np.random.choice(self.data.shape[0], K, replace=False), :self.d]
        Each_sum_in_K = [np.zeros(self.d + 1) for i in range(K)]
        same = False
        while not same:
            same = True
            for i in range(len(self.data)):
                for j in range(K):
                    dist = math.dist(self.data[i][:self.d], K_center[j])
                    if dist < self.kmeans_dist[i]:
                        self.kmeans_dist[i]=dist
                        self.kmeans_who[i]=j
                        same=False
                Each_sum_in_K[int(self.kmeans_who[i])][:self.d] += self.data[i][:self.d]
                Each_sum_in_K[int(self.kmeans_who[i])][self.d] += 1
            for i in range(K):
                if Each_sum_in_K[i][self.d] != 0:
                    K_center[i] = Each_sum_in_K[i][:self.d] / Each_sum_in_K[i][self.d]
                    Each_sum_in_K[i] = np.zeros(self.d + 1)
        σ_sum=[]       
        σ_num=[]
        for i in range(K):
            σ_sum=np.append(σ_sum,[0],axis=0)
            σ_num=np.append(σ_num,[0],axis=0)
        for dis,who in zip(self.kmeans_dist,self.kmeans_who):
            σ_sum[who] += dis
            σ_num[who] += np.array(1)
        for i in range(K):
            if σ_sum[i] != 0 and σ_num[i] != 0:
                self.neuron_group.append(Neuron(K_center[i], σ_sum[i] / σ_num[i]))
    
    def draw(self, step):
        self.sub_plot.clear()
        self.sub_plot.set_xlim(-10, 35)
        self.sub_plot.set_ylim(-5, 55)
        self.sub_plot.plot(self.road_x, self.road_y, color='green')
        self.sub_plot.plot([-6, 6], [0, 0], color='blue')
        self.sub_plot.add_patch(Rectangle((self.final_line_left_x, self.final_line_left_y), 
                                          self.final_line_width, self.final_line_height, facecolor='orange', fill=True))
        for s in self.steps_group[:step]:
            self.sub_plot.scatter(s[0][0], s[0][1], color='red', marker='o', s=4 )
        self.sub_plot.add_patch(Circle((self.steps_group[step][0][0],self.steps_group[step][0][1]), 3, color='red', fill=False))
        if self.pas==True:
            self.sub_plot.text(-60, 45, f'Success!', family='Microsoft YaHei', size=20, color='red')
        else:
            self.sub_plot.text(-60, 45, f'Please try again!', family='Microsoft YaHei', size=20, color='red')
        self.sub_plot.text(-60, 56, f'train{self.d+1}dall.txt', family='Microsoft YaHei', size=24)
        self.sub_plot.text(-60, 35, f'x:{round(self.steps_group[step][0][0], 5)}', family='Microsoft YaHei', size=15)
        self.sub_plot.text(-60, 28, f'y:{round(self.steps_group[step][0][1], 5)}', family='Microsoft YaHei', size=15)
        self.sub_plot.text(-60, 21, f'Degree:{round(math.degrees(self.steps_group[step][1]), 5)}', family='Microsoft YaHei', size=15)
        self.sub_plot.text(-60, 14, f'Front:{round(self.steps_group[step][2][0][2], 5)}', family='Microsoft YaHei', size=15)
        self.sub_plot.text(-60, 7, f'Rigsht:{round(self.steps_group[step][2][1][2], 5)}', family='Microsoft YaHei', size=15)
        self.sub_plot.text(-60, 0, f'Left:{round(self.steps_group[step][2][2][2], 5)}', family='Microsoft YaHei', size=15)
    
if __name__ == '__main__':
    RBFN(int(input('please enter 4 or 6: ')))
    while (True):
        r = input('Press Y/y to retry: ')
        if r == 'Y' or r == 'y':
            RBFN(int(input('please enter 4 or 6: ')))
        else:
            break
    #li=[(4,10),(4,15),(6,10),(6,15)]
    #for d,k in li:
    #    count=0
    #    for i in range(20):
    #        if RBFN(d,k).pas==True:
    #            count+=1
    #    print(f'{d}D.txt K: {k}  Dsuceess rate: {count}/20')
        