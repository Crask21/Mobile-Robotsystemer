import pandas as pd


df1 = pd.read_excel('log0.xlsx', sheet_name=0)

#df6 = pd.read_excel('log0.xlsx', sheet_name=0)
#df7 = pd.read_excel('log0.xlsx', sheet_name=0)
#df8 = pd.read_excel('log0.xlsx', sheet_name=0)
#df9 = pd.read_excel('log0.xlsx', sheet_name=0)




file_num = 5
count100 = 0

for i in range(file_num):
    df = pd.read_excel('log' + str(i) + '.xlsx', sheet_name=0)
    
    acc = df.loc[1][11]
    #print(acc)
    if acc == 100:
        print(acc)
        count100 += 1

print('AVG:')
print(100*count100/file_num)
