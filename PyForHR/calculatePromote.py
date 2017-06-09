<<<<<<< HEAD
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
	







	
	

=======
#/usr/local/bin
import pandas as pd
#import numpy as np
import re

df = pd.read_excel("testData.xls", sheetname = "Sheet1", index_col=0)

def getThePromote(data, groups, grade, weight):
	for group in groups:
	groupCol = list()
		for col in data.columns:
			if re.match(group, col):
				groupCol.append(col)
	groupData = data.loc[:, groupCol]
	







	
	

>>>>>>> a1535c9853bce9dc2b76b5ed253d132b0f17e45f
