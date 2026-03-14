from data_handlers import (
	retrieve_json,
	process_row,
	process_incons,
	process_fours,
	process_nans,
	process_group,
	process_meta_group,
	process_sum
	)
import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

def main():
	print("retrieving raw data")
	raw_data = retrieve_json("raw_data")
	print("processing raw data into dataframe")
	col_basic = ["n°", "colegio", "año/división", "peso", "altura"]
	test1 = list(map(lambda x: [f"t1a{x:02}",f"t1v{x:02}"], list(range(2,36))))
	col_test1 = ["t1a01"] + [item for sublist in test1 for item in sublist]
	test2 = list(map(lambda x: [f"t2a{x:02}",f"t2v{x:02}"], list(range(1,92))))
	col_test2 = [item for sublist in test2 for item in sublist]
	col_test = col_test1 + col_test2
	comment = ["comentarios"]
	col_initial = col_basic + col_test + comment
	#print(col_initial)
	df_data = pd.DataFrame(columns = col_initial)
	for key in raw_data.keys():
		#print(f"processing row {key}")
		row = process_row(key,raw_data[key])
		df_data.loc[len(df_data)] = row
	print("test 1: processing points for each section")
	test1_groups = retrieve_json("test1_groups")
	for keyg in test1_groups.keys():
		group = test1_groups[keyg]
		df_data[keyg+f" (máx:{len(group)*3})"] = process_sum(df_data,keyg,group)
		df_data[keyg+" (Nan)"] = process_nans(df_data,group,"t1a")
	print("test 1: processing total points")
	allgroup = []
	for keyg in test1_groups.keys():
		allgroup.extend(test1_groups[keyg])
	df_data[f"test1 total (máx:{len(allgroup)*3})"] = process_sum(df_data,keyg,allgroup)
	print("test 1: processing total number of NaNs")
	df_data["test1 (NaN)"] = process_nans(df_data,list(range(1,36)),"t1a")
	print("test 2: processing IN")
	incons_pairs = retrieve_json("test2_inconsistency_pairs")["0"]
	df_data["IN"] = process_incons(df_data,incons_pairs)
	print("test 2: processing IF")
	critical_fours = retrieve_json("test2_critical_fours")["0"]
	df_data["IF"] = process_fours(df_data,critical_fours,[3,5])
	print("test 2: processing NI")
	df_data["NI"] = process_fours(df_data,list(range(1,92)),[41,52])
	print("test 2: processing 12 group metrics")
	groups = retrieve_json("test2_groups")
	groups_T = retrieve_json("test2_groups_T_scores")
	for keyg in groups.keys():
		group = groups[keyg]
		T_score = groups_T[keyg]
		df_keyg,df_keyg_T = process_group(df_data,keyg,group,T_score)
		df_data[keyg+" (PD)"] = df_keyg
		df_data[keyg+" (PT)"] = df_keyg_T
		df_data[keyg+" (Nan)"] = process_nans(df_data,group,"t2v")
	print("test 2: processing number of NaNs")
	df_data["test2 (NaN)"] = process_nans(df_data,list(range(1,92)),"t2v")
	print("test 2: processing meta group metrics")
	meta_groups = retrieve_json("test2_meta_groups")
	meta_groups_T = retrieve_json("test2_meta_groups_T_scores")
	for keymg in meta_groups.keys():
		meta_group = meta_groups[keymg]
		T_score = meta_groups_T[keymg]
		limits = T_score["limits"]
		df_keymg,df_keymg_T = process_meta_group(df_data,keymg,meta_group,limits,T_score)
		df_data[keymg+" (SPT)"] = df_keymg
		df_data[keymg+" (PT)"] = df_keymg_T
	print("saving dataframe")
	df_data.to_excel('xlsx/stats.xlsx')
	return df_data

df_data = main()

"""
{
	"666":{
		"colegio":1,
		"año/división":"8Z",
		"test1":"|S|5-|34121555-|523135|55543|1454|-|322111-|",
		"peso":"-",
		"altura":"-",
		"test2":"|420110302013205331|220350150155010010|500105401010150200|105310013020015100|5022000500000020504|"
	}
}
"""
