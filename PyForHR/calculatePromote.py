#/usr/local/bin
import pandas as pd
#import numpy as np
import re

df = pd.read_excel("testData.xls", sheetname = "Sheet1", index_col=0)

def getThePromote(data = data, groups = groups, grade = grade, weight = weight):
	for group in groups:
	groupCol = list()
		for col in data.columns:
			if re.match(group, col):
				groupCol.append(col)
	groupData = data.loc[:, groupCol]
	







	
	

