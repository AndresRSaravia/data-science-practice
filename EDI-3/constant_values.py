raw_test1_values = [0,0,1,2,3]
test1_values = {x: [0,0,1,2,3] for x in range(1,36)}
test1_values[1] = None

asc = [0, 0, 1, 2, 3, 4] # True
des = [4, 3, 2, 1, 0, 0] # False

raw_test2_values = {
	1: False,
	2: True,
	3: True,
	4: True,
	5: True,
	6: True,
	7: True,
	8: True,
	9: True,
	10: True,
	11: True,
	12: False,
	13: True,
	14: True,
	15: False,
	16: True,
	17: False,
	18: True,
	19: False,
	20: False,
	21: True,
	22: False,
	23: False,
	24: True,
	25: True,
	26: False,
	27: True,
	28: True,
	29: True,
	30: False,
	31: False,
	32: True,
	33: True,
	34: True,
	35: True,
	36: True,
	37: False,
	38: True,
	39: False,
	40: True,
	41: True,
	42: False,
	43: True,
	44: True,
	45: True,
	46: True,
	47: True,
	48: True,
	49: True,
	50: False,
	51: True,
	52: True,
	53: True,
	54: True,
	55: False,
	56: True,
	57: False,
	58: False,
	59: True,
	60: True,
	61: True,
	62: False,
	63: True,
	64: True,
	65: True,
	66: True,
	67: True,
	68: True,
	69: False,
	70: True,
	71: None,
	72: True,
	73: False,
	74: True,
	75: True,
	76: False,
	77: True,
	78: True,
	79: True,
	80: False,
	81: True,
	82: True,
	83: True,
	84: True,
	85: True,
	86: True,
	87: True,
	88: True,
	89: False,
	90: True,
	91: False
}

for key in raw_test2_values.keys():
	values = raw_test2_values[key]
	if values is not None and values:
		raw_test2_values[key] = asc
	if values is not None and not values:
		raw_test2_values[key] = des

test2_values = raw_test2_values

test2_groups = {
	"DT": [1,7,11,16,25,32,49],
	"B": [4,5,28,38,46,53,61,64],
	"BD": [2,9,12,19,31,45,47,55,59,62],
	"LSE": [10,27,37,41,42,50],
	"PA": [18,20,24,56,80,84,91],
	"II": [15,23,34,57,69,73,87],
	"IA": [17,30,54,65,74,76,89],
	"ID": [8,21,26,33,40,44,51,60,77],
	"ED": [67,70,72,79,81,83,85,90],
	"P": [13,29,36,43,52,63],
	"A": [66,68,75,78,82,86,88],
	"MF": [3,6,14,22,35,39,48,58]
}

incons_pairs = [
	(2,12),(9,55),(10,50),(17,65),(21,26),
	(30,54),(31,59),(34,57),(37,41),(45,62)
]

critical_fours = [17,23,30,39,48,70,80,89,90]

"""
import pandas as pd
df_data = pd.DataFrame(columns = ["A","B"])
df_data["A"] = [2,2,3]
df_data["B"] = [1,4,34]
df_data["A-B"] = df_data.mean(axis=1)
print(df_data)
"""


