from elasticsearch import Elasticsearch

def elasticsearch_initalizer(host = "http://localhost", port = 9200):
	return Elasticsearch(HOST = host, PORT = port)

def elasticsearch_create_index(elastic_object, index_name, mappings):
	if elastic_object.indices.exists(index_name):
		elastic_object.indices.delete(index_name)

	elastic_object.indices.create(index = index_name, body = mappings)
