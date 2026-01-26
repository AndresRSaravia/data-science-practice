from data_handlers import retrieve
from constant_values import test2_values
import pandas as pd


def main():
	raw_data = retrieve('raw_data.json')
	data = pd.DataFrame({'test2question': list(range(1,92))})
	print(data)

main()