from elasticsearch import Elasticsearch

# Helper function used to make intializing the elasticsearch data store easier, provides default values if user doesn't provide their own choice.
def elasticsearch_initalizer(host = "http://localhost", port = 9200):
	return Elasticsearch(HOST = host, PORT = port)

# Helper function used to create an index on the elasticsearch object provided with the name provided and using the schema given. Deletes existing index
# if there is one before creating another as this raising IndexAlreadyExistsError from the elasticsearch API.
def elasticsearch_create_index(elastic_object, index_name, mappings):
	if elastic_object.indices.exists(index_name):
		elastic_object.indices.delete(index_name)

	elastic_object.indices.create(index = index_name, body = mappings)
