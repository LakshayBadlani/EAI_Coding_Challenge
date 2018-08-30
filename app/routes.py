from flask import request, jsonify
from app import app, validator, logic_handler

# This function utilizes the route decorator to handle all GET/POST request beginning with the signature '/contact'. 
@app.route('/contact', methods=['GET', 'POST'])
def create():
	
	# Overarching conditional statement determines what the method of the request is and sends the request to the appropriate function.
	if request.method == "POST":

		# Grabs the json formatted data stored in the payload of the post request and sends the data to be validated/inserted. Returns 
		# whether or not the insert was successful. If not a specific error message is returned along with a 400 bad request error so user
		# knows what part of the data is wrong. 

		data = request.get_json()
		return logic_handler.insert_record(data)

	elif request.method == "GET":
		
		# Grabs each of the parameters specified in the API documentation as part of the search request. If they aren't specified default to 
		# values similar to elasticsearch's own default values. Passes the parameters to seperate function that searches the database, and returns 
		# the results if they exist or errors if there are none. 

		page_size = request.args.get('pageSize', 10)

		offset = request.args.get('page', 0)

		default_query = { "query" : {
    							"match_all" : {}
  							}
						}

		query = request.args.get('query', default_query)

		return logic_handler.search_query(page_size, offset, query)

# This function utilizes the route decorator to handle all GET/DELETE/PUTS request beginning with the signature '/contact/name'. Takes the name specified
# in the URL as a parameter. 
@app.route('/contact/<string:name>', methods=['GET', "DELETE", "PUT"])
def user_manipulation(name):

	# Before determining the requests method type, check to see if the name is within the database as all these functions need that to be the case to perform 
	# properly. If it doesn't exist, return a 400 Bad Request error else allow the function to continue. 
	exists = logic_handler.contained(name)

	if not exists:
		return jsonify({'Error Message': "Contact doesn't exist in database."}), 400

	# Returns the contact information of the name specified. 
	if request.method == "GET":

		return jsonify(exists)

	# Updates the contact's information, returns a success if the operation went through, or an error specifying why the contact could not be updated.
	elif request.method == "PUT":

		data = request.get_json()

		return logic_handler.update_record(data, exists)

	# Deletes the contacts information. Always returns a success as we already check if the contact exists in the data store.
	elif request.method == "DELETE":

		logic_handler.delete_user(name)

		return jsonify({"Success": "Contact Deleted."})
