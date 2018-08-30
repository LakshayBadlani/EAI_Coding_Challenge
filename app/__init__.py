from flask import Flask
from config import Config
from elasticsearch import Elasticsearch
from app import elasticsearch_helper



app = Flask(__name__)
app.config.from_object(Config)


app.elasticsearch = elasticsearch_helper.elasticsearch_initalizer(app.config['ELASTICSEARCH_HOST'], app.config['ELASTICSEARCH_HOST'])

elasticsearch_helper.elasticsearch_create_index(app.elasticsearch, app.config['ELASTICSEARCH_IDX_NAME'], app.config['ELASTICSEARCH_SCHEMA'])

from app import routes

if __name__ == '__main__':
    app.run()