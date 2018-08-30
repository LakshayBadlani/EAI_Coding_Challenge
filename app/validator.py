from app import app
import re

def name_validator(string, regex = app.config["NAME_REGEX"]):
	""" Validates a string name passed in given the rules outlined in the README file.
	Returns: Boolean depending on if the name is valid. 
    """
	if not string or len(string.replace(" ", "")) == 0:
		return False
	if not 2 <= len(string) <= 25:
		return False
	elif not re.match(regex, string):
		return False
	else:
		return True

def email_validator(string, regex = app.config["EMAIL_REGEX"]):
	""" Validates a string email passed in given the rules outlined in the README file.
	Returns: Boolean depending on if the email is valid. 
    """
	if not string or len(string.replace(" ", "")) == 0:
		return False
	if not 6 <= len(string) <= 50:
		return False
	elif not re.match(regex, string):
		return False
	else:
		return True

def phone_number_validator(string, regex = app.config["PHONE_REGEX"]):
	""" Validates a string phone number passed in given the rules outlined in the README file.
	Returns: Boolean depending on if the phone number is valid. 
    """
	if not string or len(string.replace(" ", "")) == 0:
		return False
	if not re.match(regex, string):
		return False
	return True

def address_validator(string, regex = app.config["ADDRESS_REGEX"]):
	""" Validates a string address passed in given the rules outlined in the README file.
	Returns: Boolean depending on if the address is valid. 
    """
	if not string or len(string.replace(" ", "")) == 0:
		return False
	if not 10 <= len(string) <= 200:
		return False
	elif not re.match(regex, string, re.IGNORECASE):
		return False
	else:
		return True

def check_contains(name, ret_data = False, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME']):
	""" Checks if name exists in datastore passed in and on the index given too. Defaults to config values if none given. 
	Returns: Boolean depending on if the name is contained in the datastore. If ret_data is set to True returns the actual 
	entry in the data store.
    """
	if not name:
		return False

	q = build_query_name(name)
	search_results = es_instance.search(index = index, body = q)
	if search_results['hits']['total']:
		if ret_data:
			return search_results['hits']['hits'][0]
		return True
	return False

def build_query_name(name):
	""" Accepts a name and builds search query for that specific name.  
	Returns: Query dictionary/JSON appropriately built for elasticsearch datastore search on given name. 
    """
	query = {
	    "query": {
	        "match" : {
	            "name" : name
	        }
	    }
	}
	return query

def validate_json(data, want_to_exist = False, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME']):
	""" Takes in a data provided via JSON from the request and makes sure all the fields meeting criteria set in the README.   
	Returns: If all fields in data are valid and can be stored in the datastore return the string Passed; else return the error 
	that caused the data to be invalid.
    """
	if not data:
		return "No data was provided."

	try:
		name = data['name']
		email =  data['email']
		address = data['address']
		phone_number = data['phone_number']
	except KeyError:
		return "Some information is missing in provided input"

	# This check is necessary to differentiate between first time post requests where we dont want the name to be in our datastore 
	# already and get/put/delete requests where we do want the name to exist in the database. 
	if check_contains(name, False, es_instance = es_instance, index = index) !=  want_to_exist:
		return "Contact already in Database"
	elif not name_validator(name) or not email_validator(email) or not phone_number_validator(phone_number) or not address_validator(address):
		return "Input values for Contact not formatted correctly. Please review specifications"
	else:
		return "Passed"
