import pandas as pd, json, joblib

df = pd.read_csv('D:/ML_2/Final_Recipe_Rec/dataset_for_model.csv')         

# 2) Bỏ các cột target
targets = ['Weight_Loss','Bodybuilder','CleanEating','Diabetic',
           'Hypertension','Heart-Healthy Diet','Vegetarian','Low_Carb','None']
X = df.drop(columns=targets)

# 3) Ghi JSON
with open('models/columns.json','w') as f:
    json.dump(X.columns.tolist(), f, indent=2)

print('✓ Đã lưu models/columns.json với', len(X.columns), 'cột')
