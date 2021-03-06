import os
import sys
import re
import pandas as pd

#此函数用来检测当前目录中有没有已存在的汇总文件。
#因为下面的函数会读取所有excel文件，所以需要预先排除有没有汇总文件存在，避免读取。
#如果存在汇总文件则函数返回False，否则返回True
def ScanTargetFile():
	result = True
	pattern = r"汇总结果.xlsx"
	fileList = os.listdir('.')
	for file in fileList:
		if re.match(pattern, file):
			result = False
			break
	return result
	



#确定rulerFile为一个抬头正确的excel文件，并以这个抬头为标准,并返回这个标准抬头
def SetTheHeadRuler(rulerFile):
	df = pd.read_excel(rulerFile, 0, index_col=0, na_values= ['NA'])
	return df.columns

#此函数为传递一个标准抬头为参数，并读取当前目录下所有excel文件。
#读取的文件和标准抬头比较，如果不符合，则程序结束，提示哪个文件有问题
#如果没问题则合并并输出excel文件，名称为 ”汇总结果.xlsx"
def ReadAllExcelFiles(rulerHead):
	pattern = r"((.)+\.(xlsx|xls)$)" #Regular expression used for reading any excel file.
	fileList = os.listdir('.')
	control = True #用来控制是否将读取的多个excel数据进行合并。
	
	noTargetFileExisted = ScanTargetFile()#确定当前目录下没有汇总结果文件，如果有则这个值为False
	data = list() #用来存放所有excel文件的数据和抬头

	for file in fileList:
		if re.match(pattern, file):
		
			df = pd.read_excel(file, 0, index_col=0, na_values=['NA'])
			# 0 means to read the first sheet by default
			if not len(df.columns) == len(rulerHead):
				control = False
				print("以下文件抬头数目和标准不一致:{0}".format(file))
				break
			for col in df.columns:
				if not col in rulerHead:
					control=False
					print("以下文件抬头不统一：{0}".format(file))
					break
			data.append(df)
			
			
	print("一共读取了{0}个文件".format(len(data)))
	if control & noTargetFileExisted:
		resultData = pd.concat(data) #stack the data read from each excel file respectively
		resultData.to_excel('汇总结果.xlsx', sheet_name = 'Sheet1')
		print("已生成汇总文件！")
	elif not noTargetFileExisted:
		print("目录中存在已汇总文件，不适合生成汇总文件！请删除后重新运行！")
	else:
		print("存在错误，不适合生成汇总文件!")


def OutPutAllExcelFiles(rulerFile):
	
	rulerHead = SetTheHeadRuler(rulerFile)
	ReadAllExcelFiles(rulerHead)
		
if __name__== '__main__':
	rulerFile = sys.argv[1]#将终端第二个参数作为rulerFile传递给python3
	OutPutAllExcelFiles(rulerFile)	














