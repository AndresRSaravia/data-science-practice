import json
from constant_values import test1_values,test2_values

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
		print(answer,values)
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
	print(row_test1,row_test2)
	row = row_basic + row_test1 + row_test2 + [row_comment]
	return row
