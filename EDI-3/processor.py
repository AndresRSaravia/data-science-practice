from data_handlers import retrieve,process_row,process_group,process_incons,process_fours,process_nans
from constant_values import test2_groups,incons_pairs,critical_fours
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
	raw_data = retrieve('raw_data.json')
	columns_basic = ["n°", "año/división", "peso", "altura"]
	columns_test1 = list(map(lambda x: f"t1r{x:02}", list(range(1,36))))
	columns_test2 = list(map(lambda x: f"t2r{x:02}", list(range(1,92))))
	columns_test = columns_test1 + columns_test2
	comment = ["comentarios"]
	col_names = columns_basic + columns_test + comment
	df_data = pd.DataFrame(columns = col_names)
	for key in raw_data.keys():
		print(key)
		row = process_row(key,raw_data[key])
		df_data.loc[len(df_data)] = row
	for keyg in test2_groups.keys():
		df_data[keyg] = process_group(df_data,keyg,test2_groups[keyg])
	df_data["Inconsistencia"] = process_incons(df_data,incons_pairs)
	df_data["IF"] = process_fours(df_data,critical_fours,[3,5])
	df_data["NI"] = process_fours(df_data,list(range(1,92)),[41,52])
	df_data["test1 #nulos"] = process_nans(df_data,list(range(2,36)),"t1r")
	df_data["test2 #nulos"] = process_nans(df_data,list(range(1,92)),"t2r")
	print(df_data)
	return df_data

df_data = main()

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
