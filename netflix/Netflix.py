import sys, math, json, re
import random
from collections import OrderedDict

relative_dir	= "/u/thunt/cs373-netflix-tests/"

def get_accept_ratings():
	'''
	Returns a dictionary of the type { (movieid, customerid) : rating}
	from the probe.txt union of mv_files set
	@return void
	'''

	global relative_dir
	ratings_file	= "word-probeMapCache.txt"
	
	ratings_file = open(relative_dir + ratings_file, "r")

	movie_regexp = re.compile("^(\d+\:)")

	movies = {}

	for line in ratings_file:
		if(movie_regexp.match(line)):
			movie_id = line.split(":")[0]
		else:
			line	=	line.split("-")
			customer_id = line[0].strip()
			rating 		= int(line[1].strip())
			movies.update({(movie_id,customer_id) : rating})

	ratings_file.close()
	
	return movies

def calculate_RMSE(probe_dict, predict_keys, accept_keys):
	'''
	Helper function used for testing purposes to calculate the RMSE of the results
	@param probe_dict Dictionary form of standard input
	@param predict_keys Dictionary of the predicted results
	@param accept_keys	Dictionary of the actual results from the training file set
	'''
	keyList = probe_dict.keys()
	#length = len(keyList)
	length = 0.0
	sumt = 0.0
	
	for k in keyList:
		length = length + len(probe_dict[k])
		for cust in probe_dict[k]:
			#print(predict_keys[(k,cust)], accept_keys[(k,cust)])
			sumt = sumt + ( accept_keys[(k,cust)] - predict_keys[(k, cust)] ) ** 2

	return math.sqrt(sumt / length)

# def printDictionary(hashMap):
# 	print(json.dumps(hashMap, indent=4) )

def load_json(file_name):
	'''
	Reads in a json file to create a dictionary
	@param file_name JSON filename to be loaded
	@return dictionary form of the JSON file
	'''
	data = {}
	try:
		with open(file_name, "r") as file_handler:
			data = json.load(file_handler)
	finally:
		file_handler.close()

	return data

# def write_json(keySave, file_name):
# 	'''
# 	Writes a dictionary into a file
# 	@param keySave the dictionary to be saved
# 	@param file_name the filename used to save the dictionary
# 	@return void
# 	'''
# 	try:
# 		with open(save_dir + "/" + file_name, "w") as outfile:
# 			json.dump(keySave, outfile)
# 	finally:
# 		outfile.close()

def load_cache():
	'''
	Returns a tuple of dictionaries that load the caches average rating of movies and average ratings of customers
	@return void
	'''
	global relative_dir
	#relative_dir			= "./"

	avg_movie_cache		= "czaheri-AVG_MOVIE_RATINGS.json"
	avg_cust_cache		= "czaheri-AVG_CUST_RATING.json"

	avg_movies = load_json(relative_dir + avg_movie_cache)
	avg_cust = load_json(relative_dir + avg_cust_cache)

	return avg_movies, avg_cust

def read_input(stdin):
	'''
	Loads standard in and parses it into a dictionary of the form { movie_id : [ratings, ratings, ratings,...]}
	@param stdin Takes in standard input to be parsed
	@return dictionary
	'''
	# Redirect stdin from a file (for testing purposes), comment this out when done:
	# probetxt = "/u/thunt/cs373-netflix-tests/ericweb2-probe.txt"
	# testprobe = open(probetxt, "r")
	# stdin = testprobe

	# Load stdin into OrderedDict (preserves insertion order)
	probe_dict = OrderedDict()

	movie_regexp = re.compile("^(\d+\:)")
	
	for line in stdin:
		if(movie_regexp.match(line)):
			movie_id = line.split(":")[0]
			probe_dict.update({ movie_id : []})
		else:
			customer_id = line.strip()
			probe_dict[movie_id].append(customer_id)

	return probe_dict

def get_predict_ratings(probe_dict, avg_movies, avg_cust):
	'''
	Returns a dictionary of the predicted ratings in the form {(movie_id, customer_id) : rating}
	@param probe_dict	Standard in of the dictionary form
	@param avg_movies   Dictionary containing the average rating for all movies. Obtained from cache
	@param avg_cust     Dictionary pairing the average rating the customer has given of all the movies they have rated. Obtained from cache
	@return dictionary of results of the form {(movie_id, customer_id) : rating}
	'''
	results = {}

	keyList = probe_dict.keys()
	for mv_id in keyList:
		for customer in probe_dict[mv_id]:
			predicted = calc_rating(avg_movies[mv_id], avg_cust[customer])
			results.update({(mv_id, customer) : predicted})

	return results

def calc_rating(movie_avg, customer_avg):
	'''
	Calculates a predicted rating for the following customer by using the movie's average rating and the customer's average rating
	@param movie_avg The queried movie's average rating
	@param customer_avg The queried user's average rating
	@return floating number representing the predicted rating
	'''
	result = 0.0
	movie_offset = movie_avg - 3.7
	customer_offset = customer_avg - 3.7
	result = (3.7 + movie_offset + customer_offset)
	if(result < 1):
		result = 1
	else:
		if(result > 5):
			result = 5
	return result

def print_ratings(probe_dict, results_dict, stdout):
	'''
	Prints ratings according to specs
	@param probe_dict takes in a dictionary form coming from standard input
	@param results_dict a dictionary of the calculated results
	@param stdout standard out
	@return void
	'''
	keyList = probe_dict.keys()

	for k in keyList:
		stdout.write(k+":\n")
		for rating in probe_dict[k]:
			rate = results_dict[(k,rating)]
			stdout.write('{:.2}'.format(float(rate)) + "\n")

def drange(start, stop, step):
	'''
	Equivalent to range, but it creates a range of floating points from start to stop in the indicated steps
	@param start starting range
	@param stop  ending range
	@param step  step increments
	@return generator
	'''
	r = start
	while r < stop:
		yield r
		r += step

# def find_lowest_weights(input_dict, accept_keys, avg_movies, avg_cust):
# 	x,y = 0.0, 0.0
# 	minimum_RMSE = 20.0

# 	for c in drange(0,1, 0.001):
# 		new_predict = get_predict_ratings(input_dict, avg_movies, avg_cust, c, (1.0-c))
# 		this_RMSE = calculate_RMSE(input_dict, new_predict, accept_keys)
# 		if(this_RMSE < minimum_RMSE):
# 			minimum_RMSE = this_RMSE
# 			x = c
# 			y = 1.0 - c

# 	return x,y

# def generate_acceptances(input_dict):
# 	keyList = list(input_dict.keys())

# 	lines = 1000
# 	count = lines

# 	while(count > 0):
# 		# Pick a random movie id
# 		random.seed()
# 		amt_movies = random.randint(4, count)
# 		for t in range(amt_movies):
# 			pick_mv = random.randint(0, len(keyList)-1)
# 			mv_key = keyList[pick_mv]
# 			print(mv_key+":")
# 			count = count - 1
# 			if(count == 0):
# 				break
# 			else:
# 				random.seed()
# 				amt_cust = random.randint(0, count)
# 				for  c in range(amt_cust):
# 					cust_list = input_dict[mv_key]
# 					pick_cust = random.randint(0, len(cust_list)-1)
# 					print(cust_list[pick_cust])
# 					count = count - 1
# 					if(count == 0):
# 						break

def netflix_solve(stdin, stdout):

	# (Required) Load the cache files
	avg_movies, avg_cust = load_cache()

	# (Required) Load standard in into a dict
	input_dict = read_input(stdin)
	
	# (Required) Get predicted results into a dict
	predict = get_predict_ratings(input_dict, avg_movies, avg_cust)

	# (Not required) Uncomment the following line to calculate RMSE from a set of accepted "correct" answers
	#accept  = get_accept_ratings()

	# (Not Required) Print out a single floating number indicating the RMSE
	#print(calculate_RMSE(input_dict, predict, accept))

	# (Required) Print out the results according to the spec
	print_ratings(input_dict, predict, stdout)