def cat(input):
	headers = []
	lengths = []
	length = 0
	for line in input:
		if line.startswith('>'):
			lengths.append(length)
			line.strip()
			headers.append(line.strip())
			length = 0
		else:
			length = length + len(line.strip())
	lengths.append(length)
	del lengths[0]

	return headers, lengths

def main():
	input = open('datafile.txt','r')
	output = open('outputQ3.txt','w')

	header,lenghts = cat(input)

	for i in range(len(header)):
		output.write(header[i] + '\t'  + str(lenghts[i]) + '\n')

	output.close()

if __name__ == '__main__':
	main()
