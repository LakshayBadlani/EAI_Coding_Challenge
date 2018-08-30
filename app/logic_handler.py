from app import app, validator 
from flask import jsonify


def insert_record(data, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'],  doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):
	""" Validates the json data passed in as part of the POST's data payload. Adds it to the index specified as a parameter (or defaults) 
	and the elasticsearch datatore specified too.
	Returns: A success message including the person's name if the operation was sucessful, otherwise returns an error message that specifies
	what made the data invalid alongside a 400 Bad Request.
    """
	check = validator.validate_json(data)
	
	if check == "Passed":
		res = es_instance.index(index = index, doc_type = doc_type, body = data)
		if debug:
			return res
		return jsonify({'Added Contact': data['name']})
	else:
		if debug:
			return check
		return jsonify({'Error Message': check}), 400

def search_query(pageSize, page_offset, query, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'], doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):
	""" Finds the results that match the given query and formats it to be inline with the parameters given. 
	Returns: The formatted results if they exist. 
    """
	save = es_instance.search(index, doc_type = doc_type, body = query, size= pageSize, from_ = page_offset)

	if save and debug:
		return save
	return jsonify(save)


def contained(name, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME']):
	""" Checks to see if the datastore contains an entry linked to the name given on the index specified. 
	Returns: The entry linked to the name in the datastore, or False if it doesn't exist. 
    """
	exists = validator.check_contains(name, True, es_instance = es_instance, index = index)

	return exists

def update_record(data, record, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'], doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):
	""" Validates the json data passed in as part of the PUT's data payload. Updates the specified record on the given index in the elasticsearch datatore specified.
	Returns: A message stating the contact was updated if the operation was sucessful, otherwise returns an error message that specifies
	what made the data invalid alongside a 400 Bad Request.
    """
	check = validator.validate_json(data, want_to_exist = True, es_instance = es_instance, index = index)

	if check == "Passed":
		es_instance.update(index = index, id = record['_id'], doc_type = doc_type, body = {'doc': data})
		if debug:
			return True
		return jsonify({"Success": "Contact Updated."})
	else:
		if debug:
			return False
		return jsonify({"Error Message": check}), 400

def delete_user(name, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'], doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):
	""" Deletes the record linked to a specific name on the given index in the given datastore. 
	Returns: None if the operation is successful or a 500 error if the delete operation fails. If debug is True just return True for a sucessful delete. 
    """
	es_instance.delete_by_query(index = index, doc_type = doc_type, body={"query":{"match": {"name": name}}})

	if debug:
		return True
	return