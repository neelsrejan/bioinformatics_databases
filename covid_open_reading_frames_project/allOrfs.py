def makeRna(sequence):
	sequenceArr = list(sequence)
	for i in range(len(sequenceArr)):
		if sequenceArr[i] == 'T':
			sequenceArr[i] = 'U'
	return ''.join(sequenceArr)

def revComp(sequence):
	revComp = ''
	for i in range(len(sequence)):
		if sequence[i] == 'A':
			revComp = revComp + 'U'
		elif sequence[i] == 'U':
			revComp = revComp + 'A'
		elif sequence[i] == 'G':
			revComp = revComp + 'C'
		elif sequence[i] == 'C':
			revComp = revComp + 'G'
	return revComp

def findOrf(genome, frame):
	sequences = []
	tuples = []
	aa = {'UUU':'F', 'UUC':'F', 'UUA':'L', 'UUG':'L', 'UCU':'S', 'UCC':'S', 'UCA':'S', 'UCG':'S', 'UAU':'Y', 'UAC':'Y', 'UAA':'*', 'UAG':'*', 'UGU':'C', 'UGC':'C', 'UGA':'*', 'UGG':'W', 'CUU':'L', 'CUC':'L', 'CUA':'L', 'CUG':'L', 'CCU':'P', 'CCC':'P', 'CCA':'P', 'CCG':'P', 'CAU':'H', 'CAC':'H', 'CAA':'Q', 'CAG':'Q', 'CGU':'R', 'CGC':'R', 'CGA':'R', 'CGG':'R', 'AUU':'I', 'AUC':'I', 'AUA':'I', 'AUG':'M', 'ACU':'T', 'ACC':'T', 'ACA':'T', 'ACG':'T', 'AAU':'N', 'AAC':'N', 'AAA':'K', 'AAG':'K', 'AGU':'S', 'AGC':'S', 'AGA':'R', 'AGG':'R', 'GUU':'V', 'GUC':'V', 'GUA':'V', 'GUG':'V', 'GCU':'A', 'GCC':'A', 'GCA':'A', 'GCG':'A', 'GAU':'D', 'GAC':'D', 'GAA':'E', 'GAG':'E', 'GGU':'G', 'GGC':'G', 'GGA':'G', 'GGG':'G'}
	start = []
	end = []
	proteinSeqs = []
	combined = []
	currPos = 0
	if frame == '+':
		for j in range(3):
			for i in range(j, len(genome)-2, 3):
				codon = genome[i] + genome[i+1] + genome[i+2]
				if aa[codon] == 'M':
					start.append(i)
				if aa[codon] == '*':
					if len(start) != 0:
						if i-start[0] >= 90:
							end.append(i-1)
						else:
							start.clear()
				if len(start) != 0 and len(end) != 0:
					tuples.append([start[0], end[0], j+1])
					sequences.append(genome[start[0]:end[0]+1])
					start.clear()
					end.clear()
			
			for i in range(currPos, len(tuples)):
				seq = sequences[i]
				proteinSeq = ''
				for idx in range(0, len(seq)-2, 3):
					proteinCodon = seq[idx] + seq[idx+1] + seq[idx+2]
					proteinSeq = proteinSeq + aa[proteinCodon]
				proteinSeqs.append(proteinSeq)
			for i in range(currPos, len(tuples)):
				combined.append((tuples[i], sequences[i], proteinSeqs[i])) 
			currPos = len(tuples)
	else:
		for j in range(3):
			for i in range(len(genome)-(j+1), 1, -3):
				codon = genome[i] + genome[i-1] + genome[i-2]
				if aa[codon] == 'M':
					start.append(i)
				if aa[codon] == '*':
					if len(start) != 0:
						if start[0]-i >= 90:
							end.append(i+1)
						else:
							start.clear()
				if len(start) != 0 and len(end) != 0:
					tuples.append([end[0], start[0], -(j+1)])
					inOrder = genome[end[0]:start[0]+1]
					revOrder = inOrder[::-1]
					sequences.append(revOrder)
					start.clear()
					end.clear()
			for i in range(currPos, len(tuples)):
				seq = sequences[i][::-1]
				proteinSeq = ''
				for idx in range(len(seq)-1, 1, -3):
					proteinCodon = seq[idx] + seq[idx-1] + seq[idx-2]
					proteinSeq = proteinSeq + aa[proteinCodon]
				proteinSeqs.append(proteinSeq)
			for i in range(currPos, len(tuples)):
				combined.append((tuples[i], sequences[i], proteinSeqs[i]))
			currPos = len(tuples)

	return tuples, sequences, proteinSeqs, combined
	

def main():
	input = open('sars_cov2.fasta', 'r')
	next(input)
	genome = ''
	for line in input:
		genome = genome + line.strip()
	rnaPositiveStrand = makeRna(genome)
	rnaNegativeStrand = revComp(rnaPositiveStrand)

	posTuples, posSeqs, posProSeqs, posCombined = findOrf(rnaPositiveStrand, '+')
	negTuples, negSeqs, negProSeqs, negCombined = findOrf(rnaNegativeStrand, '-')
	
	combined = posCombined
	for i in negCombined:
		combined.append(i)

	sortedStart = sorted(combined, key = lambda x: x[0][0])
	sortedEnd = sorted(combined, key = lambda x: x[0][1])
	sortedFrame = sorted(combined, key = lambda x: x[0][2])

	outputSortedStart = open('sortedStartOrfs.txt','w')
	outputSortedEnd = open('sortedEndOrfs.txt','w')
	outputSortedFrame = open('sortedFrameOrfs.txt','w')
	outputSortedStartCombined = open('sortedStartCombinedOrfs.txt','w')
	outputSortedEndCombined = open('sortedEndCombinedOrfs.txt','w')
	outputSortedFrameCombined = open('sortedFrameCombinedOrfs.txt','w')

	for i in range(len(sortedStart)):
		outputSortedStart.write(str(sortedStart[i][0][0]+1) + ', ' + str(sortedStart[i][0][1]+1) + ', ' + str(sortedStart[i][0][2]))
		outputSortedStart.write('\n')
	
	for i in range(len(sortedEnd)):
		outputSortedEnd.write(str(sortedEnd[i][0][0]+1) + ', ' + str(sortedEnd[i][0][1]+1) + ', '+ str(sortedEnd[i][0][2]))
		outputSortedEnd.write('\n')
	
	for i in range(len(sortedFrame)):
		outputSortedFrame.write(str(sortedFrame[i][0][0]+1) + ', ' + str(sortedFrame[i][0][1]+1) + ', ' + str(sortedFrame[i][0][2]))
		outputSortedFrame.write('\n')
	
	for i in range(len(sortedStart)):
		outputSortedStartCombined.write(str(sortedStart[i][0][0]+1) + ', ' + str(sortedStart[i][0][1]+1) + ', ' + str(sortedStart[i][0][2]) + ', ' + sortedStart[i][1] + ', ' + sortedStart[i][2])
		outputSortedStartCombined.write('\n')
	
	for i in range(len(sortedEnd)):
		outputSortedEndCombined.write(str(sortedEnd[i][0][0]+1) + ', ' + str(sortedEnd[i][0][1]+1) + ', ' + str(sortedEnd[i][0][2]) + ', ' + sortedEnd[i][1] + ', ' + sortedEnd[i][2])
		outputSortedEndCombined.write('\n')
	
	for i in range(len(sortedFrame)):
		outputSortedFrameCombined.write(str(sortedFrame[i][0][0]+1) + ', ' + str(sortedFrame[i][0][1]+1) + ', ' + str(sortedFrame[i][0][2]) + ', ' + sortedFrame[i][1] + ', ' + sortedFrame[i][2])
		outputSortedFrameCombined.write('\n')

	outputSortedStart.close()
	outputSortedEnd.close()
	outputSortedFrame.close()
	outputSortedStartCombined.close()
	outputSortedEndCombined.close()
	outputSortedFrameCombined.close()

if __name__ == '__main__':
	main()
