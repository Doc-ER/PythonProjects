import pandas as pd
import os
import re

 
#注意！ 读取的excel中，如果数字是0的需要填0，不能空着。
def sumAll(excelFileList, parse_cols, skiprows, skip_footer, sheet_name, index_col=0):
	data = selectReadIn(excelFileList[0], parse_cols=parse_cols, skiprows=skiprows, 
							skip_footer=skip_footer, sheet_name=sheet_name, index_col=index_col)
	for i in range(1, len(excelFileList)):
		data += selectReadIn(excelFileList[i], parse_cols=parse_cols, skiprows=skiprows,
							 skip_footer=skip_footer, sheet_name=sheet_name, index_col=index_col,)
	return data


def selectReadIn(file, parse_cols, skiprows, skip_footer, sheet_name, index_col=0):
	data= pd.read_excel(file, sheet_name=sheet_name , parse_cols=parse_cols, skiprows=skiprows, skip_footer=skip_footer, index_col=index_col)
	return data
	
def retrieve_excel_filelist():
	excel_file_list=[]
	pattern = r'(.)+\.(xls|xlsx)$'
	file_list=os.listdir('.')
	for dir in file_list:
		if re.match(pattern, dir):
			excel_file_list.append(dir)
	return excel_file_list








if __name__ == '__main__':
	excelFileList= retrieve_excel_filelist()
	re = sumAll(excelFileList, parse_cols=list(range(2,11)), skiprows=4, skip_footer=14, sheet_name='汇总表', index_col=0)
	re.to_excel('output.xlsx', sheet_name='Sheet1')
	


									