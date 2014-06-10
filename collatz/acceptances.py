import glob, sys, re
from StringIO import StringIO
from Collatz import collatz_solve

import difflib #from difflib_data import *

path = "../collatz_tests/collatz-tests/*.in"
files = glob.glob(path)
for filename in files:
	myfile = file(filename)
	print "Opening", filename

	input = open(filename, "r")
	
	output = re.sub("\.in",".out",filename)
	output = open(output, "r")
	output_lines = [word.strip() for word in output.readlines()]
	output.close()

	old_stdout = sys.stdout
	result = StringIO()
	sys.stdout = result
	
	collatz_solve(input, result)
	#compare program's stdout to output
	sys.stdout = old_stdout

	result_lines = (result.getvalue()).splitlines()
	
	diff = difflib.unified_diff(result_lines, output_lines, lineterm='')
	
	print "\n".join(list(diff))

	result.close()
	input.close()