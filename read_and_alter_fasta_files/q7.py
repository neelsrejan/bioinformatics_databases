def howLong():
	return 'The assignment took me roughly 8 hours to complete.' + '\n' + 'I worked alone on this assignment and did not reach out for help.'


def main():
	output = open('outputQ7.txt','w')

	text = howLong()

	output.write(text + '\n')

	output.close()

if __name__ == '__main__':
	main()
