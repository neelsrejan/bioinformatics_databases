import argparse
import random

def makeRandomSeq(numSeq, sizeSeq):
	sequences = []
	countA = 0.0
	countT = 0.0
	countG = 0.0
	countC = 0.0
	for i in range(numSeq):
		sequence = ''
		for j in range(sizeSeq):
			letter = random.choice('ATGC')
			if letter == 'A':
				countA = countA + 1
			elif letter == 'T':
				countT = countT + 1
			elif letter == 'G':
				countG = countG + 1
			elif letter == 'C':
				countC = countC + 1
			sequence = sequence + letter
		sequences.append(sequence)
	freqA = countA/(numSeq*sizeSeq)
	freqT = countT/(numSeq*sizeSeq)
	freqG = countG/(numSeq*sizeSeq)
	freqC = countC/(numSeq*sizeSeq)

	return sequences, int(countA), int(countT), int(countG), int(countC), freqA, freqT, freqG, freqC

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

        return len(backtrackStr1)

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

        return backtrackArrStr2, backtrackArrStr1

def pairAlignments(sequences):
	pairs = []
	for i in range(0,len(sequences),2):
		pair = []
		pair.append(sequences[i])
		pair.append(sequences[i+1])
		pairs.append(pair)
		del pair

	lengthsP1 = []
	for pair in pairs:
		match = 1
		mismatch = -30
		indel = 0
		#print(pair)
		lengthsP1.append(locAL(pair[0], pair[1], match, mismatch, indel))

	lengthsP2 = []
	for pair in pairs:
		 match = 1
		 mismatch = -30
		 indel = -20
		 lengthsP2.append(locAL(pair[0], pair[1], match, mismatch, indel))

	return lengthsP1, lengthsP2

def indelAlignments(sequences):
	pairs = []
        for i in range(0,len(sequences),2):
                pair = []
                pair.append(sequences[i])
                pair.append(sequences[i+1])
                pairs.append(pair)
                del pair

        lengthsP1 = []
        for pair in pairs:
                match = 1 
                mismatch = -30 
                indel = 0 
                #print(pair)
                lengthsP1.append(locAL(pair[0], pair[1], match, mismatch, indel))	
	return lengthsP1

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('num_of_seq', help = 'number of random sequences desired', type =int)
	parser.add_argument('size_of_seq', help = 'length of sequence', type = int)
	args = parser.parse_args()

	numSeq = args.num_of_seq
	sizeSeq = args.size_of_seq

	sequences, countA, countT, countG, countC, freqA, freqT, freqG, freqC = makeRandomSeq(numSeq,sizeSeq)

	output = open('outputQ2SequencesAndSummary.txt', 'w')
	for i in sequences:
		output.write(i)
		output.write('\n')
	output.write('\n')

	output.write('Number of As in sequences: ')
	output.write(str(countA))
	output.write('\n')
	output.write('Frequency of As in sequences: ')
        output.write(str(freqA))
        output.write('\n')
	output.write('Number of Ts in sequences: ')
        output.write(str(countT))
        output.write('\n')
	output.write('Frequency of Ts in sequences: ')
        output.write(str(freqT))
        output.write('\n')
	output.write('Number of Gs in sequences: ')
        output.write(str(countG))
        output.write('\n')
	output.write('Frequency of Gs in sequences: ')
        output.write(str(freqG))
        output.write('\n')
	output.write('Number of Cs in sequences: ')
        output.write(str(countC))
        output.write('\n')
	output.write('Frequency of Cs in sequences: ')
        output.write(str(freqC))
        output.write('\n')
	output.close()



	P1, P2 = pairAlignments(sequences)

	output2 = open('P1AndP2_1000.txt','w')
	output2.write('Number of sequences: ')
	output2.write(str(numSeq))
	output2.write('\n')
	output2.write('Size of sequences: ')
	output2.write(str(sizeSeq))
	output2.write('\n')
	output2.write('P1: ')
	output2.write(P1)
	output2.write('\n')
	output2.write('P2: ')
	output2.write(P2)
	output2.close()

	lenArr = indelAlignments(sequences)
	output3 = open('indel_30.txt', 'w')
	output3.write('Number of sequences: ')
        output3.write(str(numSeq))
        output3.write('\n')
        output3.write('Size of sequences: ')
        output3.write(str(sizeSeq))
        output3.write('\n')
        output3.write('Lengths: ')
        output3.write(lenArr)
	output3.close()

if __name__ == '__main__':
	main()
