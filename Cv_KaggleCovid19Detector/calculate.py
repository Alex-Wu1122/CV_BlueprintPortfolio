import csv

with open("./train_study_level.csv", 'r') as file:
        csvreader = csv.reader(file)

        nfp = 0
        ta = 0
        aa = 0
        ia = 0
        nf = 0

        for row in csvreader:#計算四個分類的次數，以供觀察
                if row[1] == '1':
                        nfp += 1
                elif row[2] == '1':
                        ta += 1
                elif row[3] == '1':
                        ia += 1
                elif row[4] == '1':
                        aa += 1
                else:
                        nf += 1
        #顯示結果
        print("NFP:", nfp)
        print("TA:", ta)
        print("AA:", aa)
        print("IA:", ia)
        print("NF:", nf)
