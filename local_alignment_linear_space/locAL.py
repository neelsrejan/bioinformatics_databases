import argparse 

def locAL(str1, str2, match, mismatch, indel):
	inf = float('inf')
	dpMat = [[inf for i in range(len(str1)+1)] for j in range(len(str2)+1)]
	backMat = [[inf for i in range(len(str1)+1)] for j in range(len(str2)+1)]
	dpMat[0][0] = 0 
	backMat[0][0] = 0 
	for i in range(1, len(str1)+1):
		dpMat[0][i] = 0 
		backMat[0][i] = 'l' 
	for i in range(1, len(str2)+1):
		dpMat[i][0] = 0 
		backMat[i][0] = 'u' 
	maxVal = 0 
	maxDpMat = 0 
	max_i = 0 
	max_j = 0 
	for i in range(1, len(str2)+1):
		for j in range(1,len(str1)+1):
			dVal = inf 
			lVal = dpMat[i][j-1] + indel
			uVal = dpMat[i-1][j] + indel
			currLetStr1 = str1[j-1]
			currLetStr2 = str2[i-1]


			if currLetStr1 == currLetStr2:
				dVal = dpMat[i-1][j-1] + match
			else:
				dVal = dpMat[i-1][j-1] + mismatch

			maxVal = max(dVal, lVal, uVal)

			if maxVal == dVal:    
				if maxVal < 0:
					maxVal = 0 
					dpMat[i][j] = maxVal
					backMat[i][j] = 'd' 
				else:    
					dpMat[i][j] = maxVal
					backMat[i][j] = 'd' 
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i 
						max_j = j
			elif maxVal == lVal:    
				if maxVal < 0:
					maxVal = 0
					dpMat[i][j] = maxVal
					backMat[i][j] = 'l'
				else:
					dpMat[i][j] = maxVal
					backMat[i][j] = 'l'
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i
						max_j = j
			elif maxVal == uVal:
				if maxVal < 0:
					maxVal = 0
					dpMat[i][j] = maxVal
					backMat[i][j] = 'u'
				else:
					dpMat[i][j] = maxVal
					backMat[i][j] = 'u'
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i
						max_j = j

	backtrackArrStr2, backtrackArrStr1 = backtrackLocAL(str1, str2, maxDpMat, max_i, max_j, dpMat, backMat)
	backtrackStr2 = ''.join([i for i in backtrackArrStr2])
	backtrackStr1 = ''.join([i for i in backtrackArrStr1])

	return maxDpMat, backtrackStr1, backtrackStr2

def backtrackLocAL(str1, str2, maxDpMat, max_i, max_j, dpMat, backMat):
	backtrackArrStr2 = []
	backtrackArrStr1 = []
	maxVal = maxDpMat
	i = max_i
	j = max_j

	while maxVal != 0:
		if backMat[i][j] == 'd':
			maxVal = dpMat[i-1][j-1]
			backtrackArrStr2.insert(0, str2[i-1])
			backtrackArrStr1.insert(0, str1[j-1])
			i = i-1
			j = j-1
		elif backMat[i][j] == 'l':
			maxVal = dpMat[i][j-1]
			backtrackArrStr1.insert(0, str1[j-1])
			backtrackArrStr2.insert(0, "-")
			j = j-1
		elif backMat[i][j] == 'u':
			maxVal = dpMat[i-1][j]
			backtrackArrStr1.insert(0, "-")
			backtrackArrStr2.insert(0, str2[i-1])
			i = i-1
	return backtrackArrStr2, backtrackArrStr1

def main():
	#Parse cmdline arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('seq_file', help = 'fasta file with 2 strings to locally align')
	parser.add_argument('-m', '--match', type = int, help = 'match score', required = True)
	parser.add_argument('-s', '--mismatch', type = int, help = 'mismatch score', required = True)
	parser.add_argument('-d', '--indel', type = int, help = 'indel score', required = True)
	parser.add_argument('-a', action = 'store_true', help = 'output only the aligned sequences')
	args = parser.parse_args()

	fastaFile = args.seq_file
	match = args.match
	mismatch = args.mismatch
	indel = args.indel

	input = open(fastaFile, 'r')

	strArr = []
	for line in input:
		if line[0] != '>' and len(line.strip()) != 0:
			strArr.append(line.strip())

	str1 = strArr[0]
	str2 = strArr[1]
	maxScore, alignedStr1, alignedStr2 = locAL(str1, str2, match, mismatch, indel)

	if args.a:
		outputA = open('outputQ1A.txt','w')
		outputA.write(alignedStr1)
		outputA.write('\n')
		outputA.write(alignedStr2)
		outputA.close()
	else:
		outputnoA = open('outputQ1noA.txt','w')
		outputnoA.write(str(maxScore))
		outputnoA.write('\n')
		outputnoA.write(str(len(alignedStr1)))
		outputnoA.close()
	input.close()


if __name__ == '__main__':
	main()
