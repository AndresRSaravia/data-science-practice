# debt record
debt_record = [
	("A",14,["B"],"p1"),
	("B",13,["C"],"p2"),
	("C",12,["D"],"p3"),
	("D",11,["A"],"p4")
]

nodes = {x[0] for x in debt_record} | {c for x in debt_record for c in x[2]}
edges = {(s,t):0 for s in nodes for t in nodes}
for x in debt_record:
	for c in x[2]:
		edges[(c,x[0])] += x[1]/len(x[2])

def erase_self_debt(nodes,edges):
	self_zero = {(v,v):0 for v in nodes}
	edges.update(self_zero)

def update_debt(edges,chain,debts):
	A,B,C = chain
	a,b = debts
	changes = {}
	if a>b:
		changes[(A,B)] = a-b
		changes[(B,C)] = 0
		changes[(A,C)] = b if A!=C else 0
	elif a<b:
		changes[(A,B)] = 0
		changes[(B,C)] = b-a
		changes[(A,C)] = a if A!=C else 0
	else:
		changes[(A,B)] = 0
		changes[(B,C)] = 0
		changes[(A,C)] = a if A!=C else 0
	edges.update(changes)

is_valid = lambda A,B,value: A==B and value>0
get_valid_neigh = lambda A,edges: [
	key[1]
	for key,value in edges.items()
	if is_valid(A,key[0],value)
]
get_valid_edges = lambda edges: {
	key:value
	for key,value in edges.items()
	if value>0
}

#print("aa",(edges))
erase_self_debt(nodes,edges)
print("bb",get_valid_edges(edges))

compute_triplets = lambda edges: [
	[AB[0],AB[1],BC[1],a,b]
	for AB,a in edges.items()
	for BC,b in edges.items()
	if AB[1]==BC[0] and a>0 and b>0
]

triplets = compute_triplets(edges)
while len(triplets)!=0:
	A,B,C,a,b = triplets[0]
	print(A,B,C)
	a = edges[(A,B)]
	b = edges[(B,C)]
	print(a,b)
	print("d1",get_valid_edges(edges))
	update_debt(edges,[A,B,C],[a,b])
	print("d2",get_valid_edges(edges))
	triplets = compute_triplets(edges)


#[('D', 14.0, 'A'), ('D', 7.0, 'A'), ('C', 6.0, 'A'), ('C', 6.0, 'D'), ('A', 5.0, 'D')]


"""
	("D",14,["A"],"p1"),
	("D",14,["A","D"],"p2"),
	("C",12,["A","D"],"p3"),
	("A",5,["D"],"p4")

	("A",14,["B"],"p1"),
	("B",13,["C"],"p2"),
	("C",12,["D"],"p3"),
	("D",11,["A"],"p4")

"""
# https://billzer.com


