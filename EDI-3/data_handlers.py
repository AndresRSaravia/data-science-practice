import json
from constant_values import test1_values,test2_values
import pandas as pd
import numpy as np

def retrieve(filename):
	with open(filename, 'r') as file:
			data = json.load(file)
	return data

def get_characters(string,delchar,nonechar,extrachars=[""]):
	str_del = string.replace(delchar,"")
	str_list = list(str_del)
	result = [None if (x==nonechar or x in extrachars) else int(x) for x in str_list]
	return result

def get_values(raw_row_test,test_values,offset=0):
	n = len(raw_row_test)
	row_test = []
	for i in range(n):
		answer = raw_row_test[i]
		values = test_values[i+1]
		#print(answer,values)
		if answer is not None and values is not None:
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
	row_test1 = get_values(raw_row_test1,test1_values,1)
	row_test2 = get_values(raw_row_test2,test2_values)
	if "comentario" in raw_row.keys():
		row_comment = raw_row["comentario"]
	else:
		row_comment = None
	#print(row_test1,row_test2)
	row = row_basic + row_test1 + row_test2 + [row_comment]
	return row

def process_group(df,test_group):
	gcolumns = list(map(lambda x: f"t2r{x:02}", test_group))
	return sum(map(lambda x: df[x].apply(lambda x: x[1]), gcolumns))

def process_incons(df,pairs):
	zero_data = np.zeros((df.shape[0],1))
	df_incons = pd.DataFrame(zero_data, columns = ["Inconsistencia"])
	for (i,j) in pairs:
		dfi = df[f"t2r{i:02}"].apply(lambda x: x[1])
		dfj = df[f"t2r{j:02}"].apply(lambda x: x[1])
		#print(i,j)
		#print("i",dfi)
		#print("j",dfj)
		df_incons["Inconsistencia"] += (dfi-dfj).abs()
	typical = lambda x: ((x,"Típica") if x<19 else ((x,"Atípica") if x<23 else (x,"Muy atípica")))
	df_incons["Inconsistencia"] = df_incons["Inconsistencia"].apply(typical)
	return df_incons

def process_fours(df,answers,column_name):
	zero_data = np.zeros((df.shape[0],1))
	df_fours = pd.DataFrame(zero_data, columns = [column_name])
	print(df_fours)
	for i in answers:
		dff = df[f"t2r{i:02}"].apply(lambda x: 1 if x[1] == 4 else 0)
		print("sasssssssssssssssssss", df.shape, dff.shape, df_fours.shape)
		print("(1)", df[f"t2r{i:02}"])
		print("(2)", dff)
		print("(3)", dff+df_fours)
		df_fours += dff
	return df_fours
