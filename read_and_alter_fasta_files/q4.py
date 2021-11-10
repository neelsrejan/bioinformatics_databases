def filter(input):
	headers = []
	sequences = []
	sequence = ''
	for line in input:
		if line.startswith('>'):
			sequences.append(sequence)
			headers.append(line.strip())
			sequence = ''
		else:
			sequence = sequence + line.strip()
	sequences.append(sequence)
	del sequences[0]
	
	headersSmall = []
	for i in headers:
		headersSmall.append(i.lower())
	
	idx = 0
	idxToDel = []
	for header in headersSmall:
		if 'rat' not in header and 'mus' not in header:
			idxToDel.insert(0,idx)
		idx = idx + 1

	for i in idxToDel:
		del headers[i]
		del sequences[i]
	
	
	sequences60 = []
	for seq in sequences:
		partitionSeq = []
		lenSeq = len(seq)
		lines = lenSeq//60
		leftover = lenSeq%60
		for i in range(lines):
			partitionSeq.append([seq[60*i:60*i+60]])
		partitionSeq.append([seq[60*(lines):60*(lines)+leftover]])
		sequences60.append(partitionSeq)

	return headers, sequences60

def main():
	input = open('datafile.txt','r')
	output = open('outputQ4.txt','w')

	headers, sequences = filter(input)
	
	
	for i in range(len(headers)):
		output.write(headers[i] + '\n')
		output.write('\n')
		for j in range(len(sequences[i])):
			output.write(sequences[i][j][0] + '\n')
			output.write('\n')
		
	
	input.close()
	output.close()

if __name__ == '__main__':
	main()
