import argparse

def localLinearSpace(str1, str2, match, mismatch, indel):
	inf = float('inf')
	#first dpMat array
	dpMat = [[inf for i in range(2)] for j in range(len(str2)+1)]
	for i in range(len(str2)+1):
		dpMat[i][0] = 0
	dpMat[0][1] = 0
	
	maxDpMat = 0
	maxVal = 0
	max_i = 0
	max_j = 0
	potentialStart = []
	for i in range(1, len(str2)+1):
		dVal = 0
		if str1[0] == str2[i-1]:
			dVal = dpMat[i-1][0] + match
		else:
			dVal = dpMat[i-1][0] + mismatch
		lVal = dpMat[i][0] + indel
		uVal = dpMat[i-1][1] + indel
		
		maxVal = max(dVal, lVal, uVal)

		if maxVal == dVal:
			if maxVal < 0:
				maxVal = 0
				dpMat[i][1] = maxVal
			else:
				dpMat[i][1] = maxVal
				if dpMat[i][0] == 0:
					potentialStart.append((i-1, 0))
				if maxVal > maxDpMat:
					maxDpMat = maxVal
					max_i = i
					max_j = j
		elif maxVal == lVal:
			if maxVal < 0:
				maxVal = 0
				dpMat[i][1] = maxVal
			else:
				dpMat[i][1] = maxVal
				if dpMat[i][0] == 0:
					potentialStart.append((i, 0))
				if maxVal > maxDpMat:
					maxDpMat = maxVal
					max_i = i
					max_j = j
		elif maxVal == uVal:
			if maxVal < 0:
				maxVal = 0
				dpMat[i][1] = maxVal
			else:
				dpMat[i][1] = maxVal
				if dpMat[i-1][1] == 0:
					potentialStart.append((i-1, 1))
				if maxVal > maxDpMat:
					maxDpMat = maxVal
					max_i = i
					max_j = j


	#replace vals of mat for linear
	for i in range(1, len(str2)+1):
		dpMat[i][0] = dpMat[i][1]
		dpMat[i][1] = inf

	for j in range(2,len(str1)+1):
		for i in range(1, len(str2)+1):
			dVal = 0
			if str1[j-1] == str2[i-1]:
				dVal = dpMat[i-1][0] + match
			else:
				dVal = dpMat[i-1][0] + mismatch
			lVal = dpMat[i][0] + indel
			uVal = dpMat[i-1][1] + indel

			maxVal = max(dVal, lVal, uVal)

			if maxVal == dVal:
				if maxVal < 0:
					maxVal = 0
					dpMat[i][1] = maxVal
				else:
					dpMat[i][1] = maxVal
					if dpMat[i-1][0] == 0:
						potentialStart.append((i-1, j-1))
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i
						max_j = j
			elif maxVal == lVal:
				if maxVal < 0:
					maxVal = 0
					dpMat[i][1] = maxVal
				else:
					dpMat[i][1] = maxVal
					if dpMat[i][0] == 0:
						potentialStart.append((i, j-1))
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i
						max_j = j
			elif maxVal == uVal:
				if maxVal < 0:
					maxVal = 0
					dpMat[i][1] = maxVal
				else:
					dpMat[i][1] = maxVal
					if dpMat[i-1][1] == 0:
						potentialStart.append((i-1, j))
					if maxVal > maxDpMat:
						maxDpMat = maxVal
						max_i = i
						max_j = j

		#replace vals of mat for linear
		for i in range(1, len(str2)+1):
			dpMat[i][0] = dpMat[i][1]
			dpMat[i][1] = inf
	revStr1 = str1[::-1]
	revStr2 = str2[::-1]
	partStr1 = revStr1[len(str1)-max_j:len(str1)-potentialStart[0][1]]
	partStr2 = revStr2[len(str2)-max_i:len(str2)-potentialStart[0][0]]


	score, alignedStr1, alignedStr2 =globalAlign(partStr1, partStr2, match, mismatch, indel)
	
	return len(alignedStr1), maxDpMat, score, alignedStr1, alignedStr2
	

def globalAlign(str1, str2, match, mismatch, indel):
	inf = float('inf')
        dpMat = [[inf for i in range(len(str1)+1)] for j in range(len(str2)+1)]
        backMat = [[inf for i in range(len(str1)+1)] for j in range(len(str2)+1)]
        dpMat[0][0] = 0
        backMat[0][0] = 0
	leftVal = 0
	upVal = 0
        for i in range(1, len(str1)+1):
		leftVal = leftVal + indel
                dpMat[0][i] = leftVal 
                backMat[0][i] = 'l'
        for i in range(1, len(str2)+1):
		upVal = upVal + indel
                dpMat[i][0] = upVal
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
				dpMat[i][j] = maxVal
				if maxVal > maxDpMat:
					maxDpMat = maxVal
					max_i = i
					max_j = j
				backMat[i][j] = 'd'
			elif maxVal == lVal:
				dpMat[i][j] = maxVal
				if maxVal > maxDpMat:
                                        maxDpMat = maxVal
                                        max_i = i
                                        max_j = j
				backMat[i][j] = 'l'
			elif maxVal == uVal:
				dpMat[i][j] = maxVal
				if maxVal > maxDpMat:
                                        maxDpMat = maxVal
                                        max_i = i
                                        max_j = j
				backMat[i][j] = 'u'

        backtrackArrStr2, backtrackArrStr1 = backtrackGlobal(str1, str2, max_i, max_j, dpMat, backMat)
        revBacktrackStr2 = ''.join([i for i in backtrackArrStr2])
        revBacktrackStr1 = ''.join([i for i in backtrackArrStr1])
	backtrackStr2 = revBacktrackStr2[::-1]
	backtrackStr1 = revBacktrackStr1[::-1]
        return maxDpMat, backtrackStr1, backtrackStr2

def backtrackGlobal(str1, str2, max_i, max_j,dpMat, backMat):
        backtrackArrStr2 = []
        backtrackArrStr1 = []
        i = max_i
	j = max_j
	maxVal = float('inf')
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
        lenAlignment, localScore, globalScore, aligned1, aligned2 =localLinearSpace(str1, str2, match, mismatch, indel)
	
        output = open('outputQ4.txt','w')
        output.write('Length of alignment: ')
	output.write(str(lenAlignment))
	output.write('\n')
	output.write('Local score: ')
	output.write(str(localScore))
        output.write('\n')
	output.write('Global score: ')
	output.write(str(globalScore))
	output.write('\n')
	output.write(aligned1)
	output.write('\n')
	output.write(aligned2)
	output.close()
        input.close()
	

if __name__ == '__main__':
        main()
