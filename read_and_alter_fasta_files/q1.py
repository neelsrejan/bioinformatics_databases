def Integrity():
	return 'I have read the syllabus with the grading policy as well as the academic integrity form for this online quarter and will abide by the rules and complete my coursework with integrity.'

def main():
	output = open('outputQ1.txt','w')

	statement = Integrity()
	
	output.write(statement)
	output.write('\n')

	output.close()

if __name__ == "__main__":
	main()
