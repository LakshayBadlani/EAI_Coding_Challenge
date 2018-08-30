from flask import Flask
from config import Config
from elasticsearch import Elasticsearch
from app import elasticsearch_helper

## Initialize flask in the standard manner, and import all the settings set by the admin in the config file via a Config object so that the variables 
## can be accessed with an instance of the app. 

app = Flask(__name__)
app.config.from_object(Config)

## Starts the elasticsearch data store with the specified host name and port (from the config file) by utilizing helper functions in a seperate file.  

app.elasticsearch = elasticsearch_helper.elasticsearch_initalizer(app.config['ELASTICSEARCH_HOST'], app.config['ELASTICSEARCH_HOST'])

# Creates initial empty index on the elasticsearch object with the given schema and name from the config file. Again utilizes the helper function
# to aid with the cleanliness of code.

elasticsearch_helper.elasticsearch_create_index(app.elasticsearch, app.config['ELASTICSEARCH_IDX_NAME'], app.config['ELASTICSEARCH_SCHEMA'])

from app import routes

if __name__ == '__main__':
    app.run()