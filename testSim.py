import sim

with open ("../data/example", "r") as myfile:
	data = myfile.read().replace('\n', '')#.replace('"', '')
graph = json.loads(data)
nodes = {'Highest Degree': [['3', '0']], 'Lowest Degree': [['2', '1']]}
games = 1

print sim.run(graph, nodes, games)