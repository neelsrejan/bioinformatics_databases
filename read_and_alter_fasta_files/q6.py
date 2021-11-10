#I get 18202068 as the gi number from the query MHIQITDFGTAKVLSPDS on data.seq and data.in
#The function is built to take in the query as the first argument of argv and will manually
#load data.seq and data.in from the directory.
import sys

def getSeq(query, sequence, giIdx):
	foundIdx = []
	for i in range(len(sequence)-len(query)):
		#print(len(sequence[i:i+len(query)]))
		if sequence[i:i+len(query)] == query:
			foundIdx.append(i)

	giToReturn = []
	for j in foundIdx:
		for i in range(len(giIdx)-1):
			if j < giIdx[i+1][1]:
				giToReturn.append(giIdx[i][0])
				break
	return giToReturn

def main():
	query = sys.argv[1] 
	loadSequenceConcat = open('data.seq','r')
	loadGiIdx = open('data.in','r')
	output = open('outputQ6.txt','w')

	sequenceConcat = ''
	for line in loadSequenceConcat:
		sequenceConcat = sequenceConcat + line

	giIdx = []
	for line in loadGiIdx:
		line = line.strip()
		splitLine = line.split('\t')
		giIdx.append((int(splitLine[0]), int(splitLine[1])))

	giVals = getSeq(query, sequenceConcat, giIdx)
	
	count = 0
	for i in range(len(giVals)):
		output.write(str(giVals[i]) + '\n')
		

	loadSequenceConcat.close()
	loadGiIdx.close()
	output.close()
	

if __name__ == '__main__':
	main()
