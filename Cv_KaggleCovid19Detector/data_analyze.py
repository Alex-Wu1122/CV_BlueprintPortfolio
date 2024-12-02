import pandas as pd
df = pd.read_csv(r'C:\Users\User\Desktop\visual code\python\資科\train_image_level.csv')
df2 = pd.read_csv(r'C:\Users\User\Desktop\visual code\python\資科\train_study_level.csv')
negative_for_NaN = 0
other_for_NaN = 0
negative_for_label = 0
other_for_label = 0
for i in range(len(df['boxes'])):
    if (df['boxes'][i]!=df['boxes'][i]):
        for j in range(len(df2['id'])):
            if(df['StudyInstanceUID'][i] == df2['id'][j][:-6]):
                if(df2['Negative for Pneumonia'][j] == 1):
                    negative_for_NaN+=1
                else:
                    other_for_NaN+=1
    else:
        for j in range(len(df2['id'])):
            if(df['StudyInstanceUID'][i] == df2['id'][j][:-6]):
                if(df2['Negative for Pneumonia'][j] == 1):
                    negative_for_label+=1
                else:
                    other_for_label+=1
            
print("negative_for_NaN is ",negative_for_NaN)
print("other_for_NaN is ",other_for_NaN)
print('----------------------------')
print("negative_for_label is ",negative_for_label)
print("other_for_label is ",other_for_label)