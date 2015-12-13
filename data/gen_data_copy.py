import os, sys
from subprocess import call

def main(argv):

	if len(argv) < 3:
		print 'ERROR! not enough arguments'
		os.exit(1)

	datafile = argv[1]
	times = int(argv[2])

	os.system("rm -rf data" + str(times) + ".txt")

	for i in range(times):
		os.system("cat " + datafile + " >> data" + str(times) + ".txt")

if __name__ == "__main__":
	main(sys.argv)