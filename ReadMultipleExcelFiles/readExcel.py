import os

import pandas as pd

fileList = os.listdir('.')
fileList = fileList[1:]

data = list()
for file in fileList:
	df = pd.read_excel(file, sheetname = "Sheet1", index_col=0, na_values=['NA'])
	data.append(df)

result_data = pd.concat(data)

result_data.to_excel('汇总结果.xlsx', sheet_name = 'Sheet1')
