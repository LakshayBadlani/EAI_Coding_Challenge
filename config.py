import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

	ELASTICSEARCH_HOST = "http://localhost"
	ELASTICSEARCH_PORT = 9200
	ELASTICSEARCH_IDX_NAME = 'contacts'
	ELASTICSEARCH_SCHEMA = {
		'mappings': {
			'event' : {
				'properties': {
				'name': {'type': 'keyword'},
				'email': {'type': 'keyword'},
				'address': {'type': 'text'},
				'phone_number' : {'type': 'keyword'}
				}
			}
		}
	}
	ELASTICSEARCH_DOCTYPE = 'event'
	ADDRESS_REGEX = r'(\d*)\s*(\w+)\s+((st)|(ave)|(road)|(drive)|(street)|(avenue)+),\s+(\w*),?\s*([A-Z]{2}),\s+(\d{5})$'
	NAME_REGEX = r'^[^\W0-9_]{2,40}(?:\s[^\W0-9_]*)?\s*[^\W0-9_]{1,40}\s*$'
	EMAIL_REGEX = r"[^@;\\/]+@[^\W0-9@]+\.[^\W0-9@]+"
	PHONE_REGEX = r'^\d{9,13}$'