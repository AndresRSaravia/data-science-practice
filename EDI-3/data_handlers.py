import json

def retrieve(filename):
	with open(filename, 'r') as file:
			data = json.load(file)
	return data

def get_characters(string,delchar):
	result = string.replace(delchar,"")
	return list(result)

def process_row(key,raw_row):
	row_basic = [key,raw_row["año/división"],raw_row["peso"],raw_row["altura"]]
	row_test1 = get_characters(raw_row["test1"],"|")
	row_test2 = get_characters(raw_row["test2"],"|")
	if "comentario" in raw_row.keys():
		row_comment = raw_row["comentario"]
	else:
		row_comment = "-"
	row = row_basic + row_test1 + row_test2 + [row_comment]
	print(len(row),len(row_test1),len(row_test2),row)
	return row,row_test1,row_test2
