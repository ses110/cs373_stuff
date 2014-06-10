import io
import unittest
import random

from collections import OrderedDict

from Netflix import *

class TestNetflix(unittest.TestCase):
	def test_get_accept_ratings1(self):
		result = get_accept_ratings()
		self.assertTrue(result[('3441', '358104')] == 4)

	def test_get_accept_ratings2(self):
		result = get_accept_ratings()
		self.assertTrue(result[('708', '1182594')] == 3)

	def test_get_accept_ratings3(self):
		result = get_accept_ratings()
		self.assertTrue(result[('15657', '1300774')] == 2)

	def test_calculate_RMSE1(self):
		in_dict = {"1234" : ["1123","14567"], "5678": ["5123", "5456"]}
		predict_dict = {("1234", "1123"): 3, ("1234", "14567"): 3,("5678","5123"): 3,("5678","5456"): 3}
		accept_dict = {("1234", "1123"): 3, ("1234", "14567"): 3,("5678","5123"): 3,("5678","5456"): 3}
		rmse = calculate_RMSE(in_dict, predict_dict, accept_dict)

		self.assertTrue(rmse == 0.0)

	def test_calculate_RMSE2(self):
		in_dict = {"1234" : ["1123","14567"], "5678": ["5123", "5456"]}
		predict_dict = {("1234", "1123"): 3, ("1234", "14567"): 3,("5678","5123"): 3,("5678","5456"): 3}
		accept_dict = {("1234", "1123"): 4, ("1234", "14567"): 4,("5678","5123"): 4,("5678","5456"): 4}
		rmse = calculate_RMSE(in_dict, predict_dict, accept_dict)
		self.assertTrue(rmse == 1.0)

	def test_calculate_RMSE3(self):
		in_dict = {"1234" : ["1123","14567"], "5678": ["5123", "5456"]}
		predict_dict = {("1234", "1123"): 3, ("1234", "14567"): 3,("5678","5123"): 3,("5678","5456"): 3}
		accept_dict = {("1234", "1123"): 5, ("1234", "14567"): 5,("5678","5123"): 5,("5678","5456"): 5}
		rmse = calculate_RMSE(in_dict, predict_dict, accept_dict)
		self.assertTrue(rmse == 2.0)

	def test_load_json1(self):
		JSONfile = "/u/thunt/cs373-netflix-tests/czaheri-AVG_MOVIE_RATINGS.json"
		result = load_json(JSONfile)
		self.assertTrue(result["13356"] == 3.0)

	def test_load_json2(self):
		JSONfile = "/u/thunt/cs373-netflix-tests/czaheri-AVG_MOVIE_RATINGS.json"
		result = load_json(JSONfile)
		self.assertTrue(result["13357"] == 3.753086419753086)

	def test_load_json3(self):
		JSONfile = "/u/thunt/cs373-netflix-tests/czaheri-AVG_CUST_RATING.json"
		result = load_json(JSONfile)
		self.assertTrue(result["378466"] == 4.451553930530165)
	
	def test_read_input1(self):
		infile = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		test_dict = read_input(infile)

		infile.close()
		self.assertTrue(test_dict["1"] == ['30878', '2647871', '1283744', '2488120', '317050', '1904905', '1989766', '14756', '1027056', '1149588', '1394012', '1406595', '2529547', '1682104', '2625019', '2603381', '1774623', '470861', '712610', '1772839', '1059319', '2380848', '548064'])

	def test_read_input2(self):
		infile = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		test_dict = read_input(infile)

		infile.close()
		self.assertTrue(test_dict["10"] == ['1952305', '1531863'])

	def test_read_input3(self):
		infile = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		test_dict = read_input(infile)

		infile.close()
		self.assertTrue(test_dict["1000"] == ['2326571', '977808', '1010534', '1861759', '79755', '98259', '1960212', '97460', '2623506', '2409123', '1959111', '809597', '2251189', '537705', '929584', '506737', '708895', '1900790', '2553920', '1196779', '2411446', '1002296', '1580442', '100291', '433455', '2368043', '906984'])


	def test_get_predict_ratings1(self):
		file_in = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		input_dict = read_input(file_in)
		avg_movies, avg_cust = load_cache()
		predict = get_predict_ratings(input_dict, avg_movies, avg_cust)
		
		file_in.close()
		
		self.assertTrue(predict[('3441', '358104')] == 3.364304616076154)
	
	def test_get_predict_ratings2(self):
		file_in = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		input_dict = read_input(file_in)
		avg_movies, avg_cust = load_cache()
		predict = get_predict_ratings(input_dict, avg_movies, avg_cust)
		file_in.close()
		self.assertTrue(predict[('708', '1182594')] == 3.8136725816876678)
	
	def test_get_predict_ratings3(self):
		file_in = open("/u/thunt/cs373-netflix-tests/ericweb2-probe.txt")
		input_dict = read_input(file_in)
		avg_movies, avg_cust = load_cache()
		predict = get_predict_ratings(input_dict, avg_movies, avg_cust)
		file_in.close()
		self.assertTrue(predict[('15657', '1300774')] == 4.056430018710796)

	def test_calc_rating1(self):
		movie = 4
		cust  = 2
		rate = calc_rating(movie, cust)
		self.assertTrue(rate == 2.3)

	def test_calc_rating2(self):
		movie = 3
		cust  = 5
		rate = calc_rating(movie, cust)
		self.assertTrue(rate == 4.3)

	def test_calc_rating3(self):
		movie = 1
		cust  = 2
		rate = calc_rating(movie, cust)
		print("Rate: ", rate)
		self.assertTrue(rate == 1)


	def test_print_ratings1(self):
		w = io.StringIO()
		in_dict = OrderedDict()
		in_dict = {"1234" : ["1123","14567"], "5678": ["5123", "5456"]}
		predict_dict = {("1234", "1123"): 3, ("1234", "14567"): 3,("5678","5123"): 3,("5678","5456"): 3}
		print_ratings(in_dict, predict_dict	, w)

		self.assertTrue(w.getvalue() == "1234:\n3.0\n3.0\n5678:\n3.0\n3.0\n")

	def test_print_ratings2(self):
		w = io.StringIO()
		in_dict = OrderedDict()
		in_dict = {"10" : ["1123","14567"], "50": ["5123", "5456"]}
		predict_dict = {("10", "1123"): 3, ("10", "14567"): 3,("50","5123"): 3,("50","5456"): 3}
		print_ratings(in_dict, predict_dict	, w)

		self.assertTrue(w.getvalue() == "10:\n3.0\n3.0\n50:\n3.0\n3.0\n")


	def test_print_ratings3(self):
		w = io.StringIO()
		in_dict = OrderedDict()
		in_dict = {"10" : ["1123","14567"], "50": ["5123", "5456"]}
		predict_dict = {("10", "1123"): 3, ("10", "14567"): 3,("50","5123"): 3,("50","5456"): 3}
		print_ratings(in_dict, predict_dict	, w)

		self.assertTrue(w.getvalue() == "10:\n3.0\n3.0\n50:\n3.0\n3.0\n")
# ----
# main
# ----
if __name__ == '__main__':
	print("TestNetflix.py")
	unittest.main()
	print("Done.")