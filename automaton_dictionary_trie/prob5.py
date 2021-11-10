class Node():
	def __init__(self, val):
		self.val = val
		self.childEdges = []

class Edge():
	def __init__(self, char, towards):
		self.char = char
		self.towards = towards

def buildTrie(queries, root):
	numNodes = root.val + 1
	endNodeVal = []
	currNode = root

	for numQuery in range(len(queries)):
		currNode = root
		endNodeVal.append(numNodes-1)
	
		for letter in queries[numQuery]:
			match = False
			for edge in currNode.childEdges:
				if edge.char == letter:
					match = True
					currNode = edge.towards
					break
			if not match:
				newNode = Node(numNodes)
				newEdge = Edge(letter, newNode)
				currNode.childEdges.append(newEdge)
				numNodes = numNodes + 1
				currNode = newNode
	endNodeVal.append(numNodes-1)
	del endNodeVal[0]
	return endNodeVal

def searchTrie(root, database, endNodeVals, minLen):
	l = 0
	c = 0
	v = root
	countArr = [0 for i in range(len(endNodeVals))]
	while (l != len(database)-minLen):
		match = False
		for edge in v.childEdges:
			if (database[c] == edge.char):
				c = c + 1
				v = edge.towards
				match = True
				break
		if not match:
			if v.val in endNodeVals:
				idx = endNodeVals.index(v.val)
				countArr[idx] = countArr[idx] + 1
			l = l + 1
			c = l
			v = root
	return countArr

def main():
	input1 = open('queries.txt','r')
	input2 = open('queries2.txt', 'r')
	inputD = open('DNA.txt','r')
	queries1 = []
	queries2 = []
	database = ''
	next(inputD)
	for line in inputD:
		database = database + line.strip()
	for line in input1:
		queries1.append(line.strip())
	for line in input2:
		queries2.append(line.strip())
	minLenQuery1 = len(min((query for query in queries1 if query), key = len))
	minLenQuery2 = len(min((query for query in queries2 if query), key = len))
	queries1.sort()
	queries2.sort()
	rootQuery1 = Node(0)
	rootQuery2 = Node(0)
	endNodeValsQuery1 = buildTrie(queries1, rootQuery1)
	endNodeValsQuery2 = buildTrie(queries2, rootQuery2)
	countsQuery1 = searchTrie(rootQuery1, database, endNodeValsQuery1, minLenQuery1)
	countsQuery2 = searchTrie(rootQuery2, database, endNodeValsQuery2, minLenQuery2)

	tuplesQuery1 = []
	tuplesQuery2 = []
	for i in range(len(queries1)):
		tuplesQuery1.append((queries1[i], countsQuery1[i]))
	for i in range(len(queries2)):
		tuplesQuery2.append((queries2[i], countsQuery2[i]))
	tuplesQuery1.sort(key = lambda tup: tup[1])
	tuplesQuery2.sort(key = lambda tup: tup[1])

	outputQuery1 = open('outputQ5query1.txt', 'w')
	outputQuery2 = open('outputQ5query2.txt', 'w')
	for i in range(len(tuplesQuery1)):
		outputQuery1.write('There were ' + str(tuplesQuery1[i][1]) + ' occurances of ' + tuplesQuery1[i][0] + '.')
		outputQuery1.write('\n')
	for i in range(len(tuplesQuery2)):
		outputQuery2.write('There were ' + str(tuplesQuery2[i][1]) + ' occurances of ' + tuplesQuery2[i][0] + '.')
		outputQuery2.write('\n')
	
	inputD.close()
	input1.close()
	input2.close()
	outputQuery1.close()
	outputQuery2.close()

if __name__ == '__main__':
	main()
