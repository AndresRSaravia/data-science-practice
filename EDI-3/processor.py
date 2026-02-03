from data_handlers import retrieve,get_characters,process_row
from constant_values import test2_values,test2_groups
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
	raw_data = retrieve('raw_data.json')
	#retrieve('raw_data.json')
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
	print(df_data)
	group_data = {}
	for keyg in test2_groups.keys():
		gcolumns = list(map(lambda x: f"t2r{x:02}", test2_groups[keyg]))
		print(test2_groups[keyg])
		group_data[keyg] = sum(map(lambda x: df_data[x].apply(lambda x: x[1]), gcolumns))
	df_group = pd.concat(group_data.values(), axis=1)
	df_group.columns = group_data.keys()
	df_data = pd.concat([df_data, df_group], axis=1)
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
