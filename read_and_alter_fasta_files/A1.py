def main():
	out1 = open('outputQ1.txt','r')
	out2 = open('outputQ2.txt','r')
	out3 = open('outputQ3.txt','r')
	out4 = open('outputQ4.txt','r')
	out5a = open('outputQ5a.txt','r')
	out5b = open('outputQ5b.txt','r')
	out6 = open('outputQ6.txt','r')
	out7 = open('outputQ7.txt','r')
	A1 = open('A1.txt','w')

	outFiles = [out1, out2, out3, out4, out5a, out5b, out6, out7]
	questionTitle = ['Q1.' + '\n', 'Q2.' + '\n', 'Q3.' + '\n', 'Q4.' + '\n', 'Q5a.' + '\n', 'Q5b.' + '\n', 'Q6.' + '\n', 'Q7.' + '\n']
	for i in range(len(outFiles)):
		A1.write(questionTitle[i])
		for line in outFiles[i]:
			A1.write(line)
		A1.write('\n')
		A1.write('\n')
	A1.close()

if __name__ == '__main__':
	main()
