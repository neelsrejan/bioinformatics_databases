def index(input):
	headersGiNum = []
	sequenceLenArr = []
	sequence = ''
	for line in input:
		if line.startswith('>'):
			sequenceLenArr.append(len(sequence))
			line = line.strip()

			headerGi = line[4:]
			delimiterIdx = headerGi.index('|')

			giNum = headerGi[:delimiterIdx]
			headersGiNum.append(giNum)
			sequence = ''
		else:
			sequence = sequence + line.strip()
	sequenceLenArr.append(len(sequence))
	del sequenceLenArr[0]

	idxArr = [0]
	idx = 0
	for i in range(len(sequenceLenArr)):
		idx = idx + sequenceLenArr[i] + 1
		idxArr.append(idx)
	del idxArr[-1]

	return headersGiNum, idxArr

def main():
	input = open('datafile.txt','r')
	output = open('data.in','w')

	giNum, startIdx = index(input)

	for i in range(len(giNum)):
		output.write(str(giNum[i]) + '\t' + str(startIdx[i]) + '\n')

	input.close()
	output.close()

if __name__ == '__main__':
        main()
