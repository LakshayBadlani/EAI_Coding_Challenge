from flask import request, jsonify
from app import app, validator, logic_handler


@app.route('/contact', methods=['GET', 'POST'])
def create():
	
	if request.method == "POST":

		data = request.get_json()
		return logic_handler.insert_record(data)

	elif request.method == "GET":
		
		page_size = request.args.get('pageSize', 10)

		offset = request.args.get('page', 0)

		default_query = { "query" : {
    							"match_all" : {}
  							}
						}

		query = request.args.get('query', default_query)

		return logic_handler.search_query(page_size, offset, query)

@app.route('/contact/<string:name>', methods=['GET', "DELETE", "PUT"])
def user_manipulation(name):

	exists = logic_handler.contained(name)

	if not exists:
		return jsonify({'Error Message': "Contact doesn't exist in database."}), 400

	if request.method == "GET":

		return jsonify(exists)

	elif request.method == "PUT":

		data = request.get_json()

		return logic_handler.update_record(data, exists)

	elif request.method == "DELETE":

		logic_handler.delete_user(name)

		return jsonify({"Success": "Contact Deleted."})
