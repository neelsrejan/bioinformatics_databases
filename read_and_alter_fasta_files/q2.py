# I will be using python as my scipting language as well as vim as my text editor and will be running everything through mac terminal. 
def Hello():
	return 'Hello Bioinformatics'

def main():
	output = open('outputQ2.txt','w')
	
	hi = Hello()

	output.write(hi)
	output.write('\n')

	output.close()

if __name__ == "__main__":
	main()
