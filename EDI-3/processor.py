from data_handlers import (
	retrieve_json,
	process_row,
	process_incons,
	process_fours,
	process_nans,
	process_group,
	process_meta_group,
	process_proportions
	)
import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

def main():
	print("retrieving raw data")
	raw_data = retrieve_json("raw_data")
	print("processing raw data into ")
	columns_basic = ["colegio", "n°", "año/división", "peso", "altura"]
	columns_test1 = list(map(lambda x: f"t1r{x:02}", list(range(1,36))))
	columns_test2 = list(map(lambda x: f"t2r{x:02}", list(range(1,92))))
	columns_test = columns_test1 + columns_test2
	comment = ["comentarios"]
	columns_initial = columns_basic + columns_test + comment
	df_data = pd.DataFrame(columns = columns_initial)
	for key in raw_data.keys():
		print(f"processing row {key}")
		row = process_row(key,raw_data[key])
		df_data.loc[len(df_data)] = row
	print("test 1: processing mean for each section")
	test1_groups = retrieve_json("test1_groups")
	for keyg in test1_groups.keys():
		group = test1_groups[keyg]
		df_data[keyg] = process_proportions(df_data,keyg,group)
		df_data[keyg+" (Nan)"] = process_nans(df_data,group,"t1r")
	print("test 1: processing number of NaNs")
	df_data["test1 (NaN)"] = process_nans(df_data,list(range(1,36)),"t1r")
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
		df_data[keyg] = process_group(df_data,keyg,group,T_score)
		df_data[keyg+" (Nan)"] = process_nans(df_data,group,"t2r")
	print("test 2: processing number of NaNs")
	df_data["test2 (NaN)"] = process_nans(df_data,list(range(1,92)),"t2r")
	print("test 2: processing meta group metrics")
	meta_groups = retrieve_json("test2_meta_groups")
	meta_groups_T = retrieve_json("test2_meta_groups_T_scores")
	for keymg in meta_groups.keys():
		meta_group = meta_groups[keymg]
		T_score = meta_groups_T[keymg]
		limits = T_score["limits"]
		#print(keymg,meta_group,T_score,limits)
		df_data[keymg] = process_meta_group(df_data,keymg,meta_group,limits,T_score)
	#T12_scores = retrieve_json("T12_scores")
	#print(df_data)
	return df_data

df_data = main()
df_data.to_excel('xlsx/stats.xlsx')

"""
{
	"666":{
		"año/división":"8Z",
		"test1":"|S|5-|34121555-|523135|55543|1454|-|322111-|",
		"peso":"-",
		"altura":"-",
		"test2":"|420110302013205331|220350150155010010|500105401010150200|105310013020015100|5022000500000020504|"
	}
}
"""
