import sys, math, json, re
from collections import OrderedDict

def rmse_sum_gen_zip (a, p) :
    """
    O(1) in space
    O(n) in time
    """
    s = len(a)
    z = zip(a, p)
    v = sum(((x - y) ** 2 for x, y in z), 0.0)
    return math.sqrt(v / s)

def get_accept_ratings():
	'''
	Returns a dictionary of the type { (movieid, customerid) : rating}
	from the probe.txt union of mv_files set
	'''

	relative_dir	= "/u/thunt/cs373-netflix-tests/"
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

	return movies

def calculate_RMSE(probe_dict, predict_keys, accept_keys):
	keyList = probe_dict.keys()
	length = len(keyList)
	sumt = 0.0
	
	for k in keyList:
		length = length + len(probe_dict[k])
		for cust in probe_dict[k]:
			#print(predict_keys[(k,cust)], accept_keys[(k,cust)])
			sumt = sumt + ( accept_keys[(k,cust)] - predict_keys[(k, cust)] ) ** 2

	return math.sqrt(sumt / length)

def printDictionary(hashMap):
	print(json.dumps(hashMap, indent=4) )

def load_json(file_name):
	'''
	Reads in a json file to create a dictionary
	'''
	try:
		with open(file_name, "r") as file_handler:
			data = json.load(file_handler)
	finally:
		file_handler.close()

	return data

def write_json(keySave, file_name):
	try:
		with open(save_dir + "/" + file_name, "w") as outfile:
			json.dump(keySave, outfile)
	finally:
		outfile.close()

def load_cache():
	relative_dir			= "/u/thunt/cs373-netflix-tests/"
	#relative_dir			= "./"

	avg_movie_cache		= "czaheri-AVG_MOVIE_RATINGS.json"
	avg_cust_cache		= "czaheri-AVG_CUST_RATING.json"

	avg_movies = load_json(relative_dir + avg_movie_cache)
	avg_cust = load_json(relative_dir + avg_cust_cache)

	return avg_movies, avg_cust


def read_input(stdin):
	probetxt = "/u/thunt/cs373-netflix-tests/ericweb2-probe.txt"
	testprobe = open(probetxt, "r")
	stdin = testprobe


	avg_movies, avg_cust = load_cache()

	# Load stdin into OrderedDict (preserves insertion order)
	probe_dict = OrderedDict()

	movie_regexp = re.compile("^(\d+\:)")
	
	for line in stdin:
		if(movie_regexp.match(line)):
			movie_id = line.split(":")[0]
			probe_dict.update({ movie_id : []})
		else:
			customer_id = line.strip()
			# calc_rating(avg_movies[movie_id], avg_cust[customer_id])

			probe_dict[movie_id].append(customer_id)

	return probe_dict

def get_predict_ratings(probe_dict, avg_movies, avg_cust, x=0.5, y=0.5):
	results = {}

	keyList = probe_dict.keys()
	for mv_id in keyList:
		for customer in probe_dict[mv_id]:
			predicted = calc_rating(avg_movies[mv_id], avg_cust[customer], x,y)
			results.update({(mv_id, customer) : predicted})

	return results

def calc_rating(movie_avg, customer_avg, x=0.5,y=0.5):
	#print("movie_avg: " + str(movie_avg) +  " customer_avg " + str(customer_avg))
	return (0.53*customer_avg + 0.47*movie_avg)
	#return 3.7

def print_ratings(probe_dict, results_dict, stdout):
	keyList = probe_dict.keys()
	limit = 0

	for k in keyList:
		print(k+":")
		for rating in probe_dict[k]:
			print(results_dict[(k,rating)])

		limit = limit + 1
		if(limit == 2):
			break

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step

def find_lowest_weights(input_dict, accept_keys, avg_movies, avg_cust):
	x,y = 0.0, 0.0
	minimum_RMSE = 20.0

	for c in drange(0,1, 0.001):
		new_predict = get_predict_ratings(input_dict, avg_movies, avg_cust, c, (1.0-c))
		this_RMSE = calculate_RMSE(input_dict, new_predict, accept_keys)
		if(this_RMSE < minimum_RMSE):
			minimum_RMSE = this_RMSE
			x = c
			y = 1.0 - c

	return x,y

def netflix_solve(stdin, stdout):
	avg_movies, avg_cust = load_cache()
	input_dict = read_input(stdin)
	
	#predict = get_predict_ratings(input_dict, avg_movies, avg_cust)
	accept  = get_accept_ratings()
	print(find_lowest_weights(input_dict, accept, avg_movies, avg_cust))
	#print(calculate_RMSE(input_dict, predict, accept))
	#print_ratings(input_dict, predict, stdout)