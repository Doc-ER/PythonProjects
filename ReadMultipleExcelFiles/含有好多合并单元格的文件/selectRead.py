import pandas as pd

file = pd.read_excel('test1.xls', sheet_name='Sheet1', parse_cols=list(range(2,11)), 
							index_col=0, skiprows= 4, skip_footer= 14)



									