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
	if frame == '+':
		for i in range(0, len(genome)-2, 3):
			codon = genome[i] + genome[i+1] + genome[i+2]
			#print(codon)
			if aa[codon] == 'M':
				start.append(i)
			if aa[codon] == '*':
				if len(start) != 0:
					if i-start[0] >= 90:
						end.append(i-1)
					else:
						#del start[0]
						start.clear()
			if len(start) != 0 and len(end) != 0:
				tuples.append([start[0], end[0], frame])
				sequences.append(genome[start[0]:end[0]+1])
				#del start[0]
				#del end[0]
				start.clear()
				end.clear()
		
		for seq in sequences:
			proteinSeq = ''
			for idx in range(0, len(seq)-2, 3):
				proteinCodon = seq[idx] + seq[idx+1] + seq[idx+2]
				proteinSeq = proteinSeq + aa[proteinCodon]
			proteinSeqs.append(proteinSeq)
		for i in range(len(tuples)):
			combined.append((tuples[i], sequences[i], proteinSeqs[i])) 
	else:
		for i in range(len(genome)-1, 1, -3):
			codon = genome[i] + genome[i-1] + genome[i-2]
			if aa[codon] == 'M':
				start.append(i)
			if aa[codon] == '*':
				if len(start) != 0:
					if start[0]-i >= 90:
						end.append(i+1)
					else:
						#del start[0]
						start.clear()
			if len(start) != 0 and len(end) != 0:
				tuples.append([end[0], start[0], frame])
				sequences.append(genome[end[0]:start[0]+1])
				#del start[0]
				#del end[0]
				start.clear()
				end.clear()
		for seq in sequences:
			proteinSeq = ''
			for idx in range(len(seq)-1, 1, -3):
				proteinCodon = seq[idx] + seq[idx-1] + seq[idx-2]
				proteinSeq = proteinSeq + aa[proteinCodon]
				#proteinSeqSorted = proteinSeq[::-1]
			proteinSeqs.append(proteinSeq)
		for i in range(len(tuples)):
			combined.append((tuples[i], sequences[i], proteinSeqs[i]))

	#print(start)
	#print(end)
	#print(tuples)
	#print(sequences)
	#print(len(tuples))
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
	
	positivesCombined = list(zip(posTuples, posSeqs, posProSeqs))
	negativesCombined = list(zip(negTuples, negSeqs, negProSeqs))

	combined = posCombined
	for i in negCombined:
		combined.append(i)
	print(combined)
	print('\n')

	sortedStrand = combined
	sortedStart = sorted(combined, key = lambda x: x[0][0])
	sortedEnd = sorted(combined, key = lambda x: x[0][1])
	print('Sorted by start')
	print(sortedStart)
	print('\n')
	print('Sorted by end')
	print(sortedEnd)
	print('\n')
	print('Sorted by strand')
	print(sortedStrand)
	print('\n')
	print(len(posTuples))
	print(len(negTuples))
	'''
	#print(rnaNegWord3)
	word = 'AUUUAGCCUAUGUUUCUAGUAUAAGAAAUGCGGAAAUCCAUGUGAUAGACUAUGCUUGCAUAAGCA'
	#word2 = 'AUUUUACCUCAUUUUGUAGCAUCACUGCAUCGGAAAUCCCAUUUAUCAGUGCAUCCCGGGCUAUUU'
	word2 = 'UUUCUAGGGCCCCAUGUGUCAUUACAUUCCAAACGGCAUCUGUCAGCAGUAUUUCAUCCUUUAAUU'
	rnaWord = makeRna(word)
	rnaWord2 = makeRna(word2)
	rnaNegWord2 = revComp(rnaWord2)
	positiveTuples, positiveSequences, posProteinSequences, posCombined = findOrf(rnaWord, '+')
	negativeTuples, negativeSequences, negProteinSequences, negCombined = findOrf(rnaNegWord2, '-')
	positiveCombined = list(zip(positiveTuples, positiveSequences, posProteinSequences))
	negativeCombined = list(zip(negativeTuples, negativeSequences, negProteinSequences))
	
	combined = posCombined
	for i in negCombined:
		combined.append(i)
	print(combined)
	print('\n')
	
	sortedStrand = combined
	sortedStart = sorted(combined, key = lambda x: x[0][0])
	sortedEnd = sorted(combined, key = lambda x: x[0][1])
	print(sortedStart)
	print('\n')
	print(sortedEnd)
	print('\n')
	print(sortedStrand)
	print('\n')
	'''

if __name__ == '__main__':
	main()
