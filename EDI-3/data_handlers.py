import json
from constant_values import test1_values,test2_values

def retrieve(filename):
	with open(filename, 'r') as file:
			data = json.load(file)
	return data

def get_characters(string,delchar,nonechar,extrachars=[""]):
	str_del = string.replace(delchar,"")
	str_list = list(str_del)
	clean = lambda x: None if x==nonechar else (x if x in extrachars else int(x))
	result = [clean(x) for x in str_list]
	return result

def get_values(raw_row_test,test_values,offset=0,extrachars=[""]):
	n = len(raw_row_test)
	row_test = []
	for i in range(n):
		answer = raw_row_test[i]
		values = test_values[i+1]
		#print(answer,values)
		if answer in extrachars:
			row_test.append(answer)
		elif answer is not None and values is not None:
			row_test.append((answer,values[answer-offset]))
		elif answer is not None and values is None:
			row_test.append((answer,None))
		else:
			row_test.append((None,None))
	return row_test

def process_row(key,raw_row):
	row_basic = [key,raw_row["año/división"],raw_row["peso"],raw_row["altura"]]
	raw_row_test1 = get_characters(raw_row["test1"],"|","-",extrachars=["S","N"])
	raw_row_test2 = get_characters(raw_row["test2"],"|","-")
	row_test1 = get_values(raw_row_test1,test1_values,1,["S","N"])
	row_test2 = get_values(raw_row_test2,test2_values)
	if "comentario" in raw_row.keys():
		row_comment = raw_row["comentario"]
	else:
		row_comment = None
	row = row_basic + row_test1 + row_test2 + [row_comment]
	return row

def process_group(df,keyg,test_group):
	gcolumns = list(map(lambda x: f"t2r{x:02}", test_group))
	df_keyg = sum(map(lambda x: df[x].apply(lambda x: x[1]), gcolumns))
	return df_keyg

def typical(x,limit1,limit2):
	if x<limit1:
		tup = (x,"Típica")
	elif x<limit2:
		tup = (x,"Atípica")
	else:
		tup = (x,"Muy atípica")
	return tup

def process_incons(df,pairs):
	df_incons = 0
	for (i,j) in pairs:
		dfi = df[f"t2r{i:02}"].apply(lambda x: x[1])
		dfj = df[f"t2r{j:02}"].apply(lambda x: x[1])
		#print(i,j)
		#print("i",dfi)
		#print("j",dfj)
		df_incons += (dfi-dfj).abs()
	df_incons = df_incons.apply(lambda x: typical(x,19,23))
	return df_incons

def process_fours(df,answers,limits):
	limit1,limit2 = limits
	df_fours = 0
	for answer in answers:
		dff = df[f"t2r{answer:02}"].apply(lambda x: 1 if x[1] == 4 else 0)
		#print("(1)", df[f"t2r{answer:02}"])
		#print("(2)", dff)
		#print("(3)", dff+df_fours)
		df_fours += dff
	df_fours = df_fours.apply(lambda x: typical(x,limit1,limit2))
	return df_fours

def process_nans(df,columns,tag):
	df_nans = 0
	for column in columns:
		df_nans += df[f"{tag}{column:02}"].apply(lambda x: x[0]).isna().apply(lambda x: 1 if x else 0)
	return df_nans