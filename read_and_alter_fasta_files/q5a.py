def makeSeq(input):
	sequences = []
	sequence = ''
	for line in input:
		if line.startswith('>'):
			sequences.append(sequence)
			sequence = ''
		else:
			sequence = sequence + line.strip()
	sequences.append(sequence)
	del sequences[0]

	longSeq = ''
	for i in sequences:
		longSeq = longSeq + i + '@'
	longSeq = longSeq[:-1]

	return longSeq

def main():
	input = open('datafile.txt','r')
	output = open('data.seq','w')

	longSeq = makeSeq(input)

	output.write(longSeq)

	input.close()
	output.close()

if __name__ == '__main__':
	main()
