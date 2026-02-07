import json

def retrieve_json(filename):
	with open("json/"+filename+".json", "r") as file:
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
		values = test_values[str(i+1)]
		#print(i,answer,values)
		if answer in extrachars:
			row_test.append(answer)
		elif (answer is not None) and (values is not None):
			row_test.append((answer,values[answer-offset]))
		elif (answer is not None) and (values is None):
			row_test.append((answer,None))
		else:
			row_test.append((None,None))
	return row_test

def process_row(key,raw_row):
	row_basic = [key,raw_row["año/división"],raw_row["peso"],raw_row["altura"]]
	raw_row_test1 = get_characters(raw_row["test1"],"|","-",extrachars=["S","N"])
	raw_row_test2 = get_characters(raw_row["test2"],"|","-")
	test1_values = retrieve_json("test1_values")
	test2_values = retrieve_json("test2_values")
	is_no_value = lambda x: x if x != "no value" else None
	test1_values = {x:is_no_value(test1_values[x]) for x in test1_values.keys()}
	test2_values = {x:is_no_value(test2_values[x]) for x in test2_values.keys()}
	row_test1 = get_values(raw_row_test1,test1_values,1,["S","N"])
	row_test2 = get_values(raw_row_test2,test2_values)
	if "comentario" in raw_row.keys():
		row_comment = raw_row["comentario"]
	else:
		row_comment = None
	row = row_basic + row_test1 + row_test2 + [row_comment]
	return row

def process_nans(df,columns,tag):
	df_nans = 0
	bool_to_int = lambda x: int(x)
	ncolumns = list(map(lambda x: f"{tag}{x:02}", columns))
	for keyn in ncolumns:
		df_nans += df[keyn].apply(lambda x: x[0]).isna().apply(bool_to_int)
	tuple_form = lambda x: (x,len(columns),round(x/len(columns),3))
	df_nans = df_nans.apply(tuple_form)
	return df_nans

def process_proportions(df,keyg,group):
	gcolumns = list(map(lambda x: f"t1r{x:02}", group))
	#print(df[gcolumns])
	df_keyg = sum(map(lambda x: df[x].apply(lambda x: x[1]), gcolumns))
	tuple_form = lambda x: (x,len(gcolumns),round(x/len(gcolumns),3))
	df_keyg = df_keyg.apply(tuple_form)
	return df_keyg

def process_group(df,keyg,group,T_score):
	gcolumns = list(map(lambda x: f"t2r{x:02}", group))
	if_none_zero = lambda x: x if x is not None else 0
	df_keyg = sum(map(lambda x: df[x].apply(lambda x: if_none_zero(x[1])), gcolumns))
	df_keyg = df_keyg.apply(lambda x: (x,T_score[str(int(x))]))
	return df_keyg

def process_meta_group(df,keymg,meta_group): #,T_score
	mgcolumns = list(map(lambda x: f"{x}", meta_group))
	df_keymg = sum(map(lambda x: df[x].apply(lambda x: x[1]), mgcolumns))
	df_keymg = df_keymg.apply(lambda x: (x)) #,T_score[str(int(x))]
	return df_keymg

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
