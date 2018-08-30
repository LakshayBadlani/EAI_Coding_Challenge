from app import app, validator 
from flask import jsonify

def insert_record(data, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'],  doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):
	
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

def search_query(pageSize, page_offset, query, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'], doc_type = app.config['ELASTICSEARCH_DOCTYPE']):
	
	return jsonify(es_instance.search(index, doc_type = doc_type, body = query, size= pageSize, from_ = page_offset))

def contained(name, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME']):

	exists = validator.check_contains(name, True, es_instance = es_instance, index = index)

	return exists

def update_record(data, record, es_instance = app.elasticsearch, index = app.config['ELASTICSEARCH_IDX_NAME'], doc_type = app.config['ELASTICSEARCH_DOCTYPE'], debug = False):

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

	es_instance.delete_by_query(index = index, doc_type = doc_type, body={"query":{"match": {"name": name}}})

	if debug:
		return True
	return