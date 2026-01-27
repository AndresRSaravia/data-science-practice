from data_handlers import retrieve,get_characters,process_row
from constant_values import test2_values,test2_groups
import pandas as pd


def main():
	raw_data = {
		"666":{
			"año/división":"8Z",
			"test1":"|S|5-|34121555-|523135|55543|1454|-|322111-|",
			"peso":"-",
			"altura":"-",
			"test2":"|420110302013205331|220350150155010010|500105401010150200|105310013020015100|5022000500000020504|"
		}
	}
	#retrieve('raw_data.json')
	columns_basic = ["n°", "año/división", "peso", "altura"]
	columns_test1 = list(map(lambda x: f"t1r{x:02}", list(range(1,36))))
	columns_test2 = list(map(lambda x: f"t2r{x:02}", list(range(1,92))))
	columns_test = columns_test1 + columns_test2
	comment = ["comentarios"]
	columns_group = ["DT","B","BD","LSE","PA","II","IA","ID","ED","P","A","MF"]
	col_names = columns_basic + columns_test + comment + columns_group
	df_data = pd.DataFrame(columns = col_names)
	print(df_data)
	for key in raw_data.keys():
		print(key)
		row,row_test1,row_test2 = process_row(key,raw_data[key])
		row_group = []
		for keyg in test2_groups.keys():
			value_group = 0
			qindexes = test2_groups[keyg]
			for qindex in qindexes:
				print(qindex,int(row_test2[qindex-1]),test2_values,row_test2)
				if row_test2[qindex-1]!="-":
					value_group += test2_values[qindex][int(row_test2[qindex-1])]
			row_group += [value_group]
		df_data.loc[len(df_data)] = row + row_group
	print(df_data)

main()

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
