import unittest
import json
from app import app, validator, elasticsearch_helper, logic_handler
from config import Config
from elasticsearch import Elasticsearch

# Tests name validation thoroughly on a number of different cases and makes sure the validator returns the appropriate response based on predetermined criteria. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestNameValidation(unittest.TestCase):
	
	name_regex_for_testing = r'^[^\W0-9_]{2,40}(?:\s[^\W0-9_]*)?\s*[^\W0-9_]{1,40}\s*$'

	def test_empty_string(self):
		self.assertFalse(validator.name_validator("", self.name_regex_for_testing))

	def test_only_numbers_in_name(self):
		self.assertFalse(validator.name_validator("12345", self.name_regex_for_testing))

	def test_only_letters_in_name(self):
		self.assertTrue(validator.name_validator("Lakshay Badlani", self.name_regex_for_testing))

	def test_only_letters_and_numbers_in_name(self):
		self.assertFalse(validator.name_validator("Lak6h3y 7adlani", self.name_regex_for_testing))

	def test_only_white_space_in_name(self):
		self.assertFalse(validator.name_validator("      ", self.name_regex_for_testing))
	
	def test_special_characters_in_name(self):
		self.assertFalse(validator.name_validator("La^%Kshay", self.name_regex_for_testing))

	def test_first_name_only_in_name(self):
		self.assertTrue(validator.name_validator("Lakshay", self.name_regex_for_testing))

	def test_first_name_and_whitespace_in_name(self):
		self.assertTrue(validator.name_validator("Lakshay ", self.name_regex_for_testing))

	def test_name_too_short(self):
		self.assertFalse(validator.name_validator("L", self.name_regex_for_testing))
	
	def test_name_too_long(self):
		self.assertFalse(validator.name_validator("Lakshay lakshay lakshay lakshay lakshay lakshay lakshay lakshay", self.name_regex_for_testing))

	def test_middle_name_included(self):
		self.assertTrue(validator.name_validator("Lakshay Mohanlal Badlani", self.name_regex_for_testing))

	def test_middle_name_and_whitespace_included(self):
		self.assertTrue(validator.name_validator("Lakshay Mohanlal ", self.name_regex_for_testing))
	
	def test_only_middle_name(self):
		self.assertFalse(validator.name_validator("Lakshay Mohanlal Mohanlal Badlani", self.name_regex_for_testing))
	
	def test_full_name_and_whitespace_included(self):
		self.assertTrue(validator.name_validator("Lakshay Mohanlal Badlani ", self.name_regex_for_testing))

# Tests email validation thoroughly on a number of different cases and makes sure the validator returns the appropriate response based on predetermined criteria. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestEmailValidation(unittest.TestCase):
	
	email_regex_for_testing = r"[^@;\\/]+@[^\W0-9@]+\.[^\W0-9@]+"

	def test_empty_string(self):
		self.assertFalse(validator.email_validator("", self.email_regex_for_testing))

	def test_bad_special_characters_in_email(self):
		self.assertFalse(validator.email_validator("l;badlani@gmail.com", self.email_regex_for_testing))

	def test_normal_email(self):
		self.assertTrue(validator.email_validator("lbadlani@gmail.com", self.email_regex_for_testing))

	def test_allowed_special_characters(self):
		self.assertTrue(validator.email_validator("l.bad_lani@gmail.com", self.email_regex_for_testing))

	def test_only_white_space_in_email(self):
		self.assertFalse(validator.email_validator("      ", self.email_regex_for_testing))
	
	def test_no_at_in_email(self):
		self.assertFalse(validator.email_validator("lakshaygmail.com", self.email_regex_for_testing))

	def test_too_short_email(self):
		self.assertFalse(validator.email_validator("l@.com", self.email_regex_for_testing))

	def test_too_long_email(self):
		self.assertFalse(validator.email_validator("Lakshaylakshaylakshaylakshaylakshaylakshay@gmailgmail.com", self.email_regex_for_testing))

	def test_dot_com_at_end(self):
		self.assertTrue(validator.email_validator("l.badlani@gmail.com", self.email_regex_for_testing))
	
	def test_alternate_domain(self):
		self.assertTrue(validator.email_validator("l.badlan@berkeley.edu", self.email_regex_for_testing))

	def test_no_domain_given(self):
		self.assertFalse(validator.email_validator("l.badlani@com", self.email_regex_for_testing))

	def test_not_fully_formed(self):
		self.assertFalse(validator.email_validator("l.badlani@", self.email_regex_for_testing))
	
	def test_short_domain(self):
		self.assertTrue(validator.email_validator("l.badlani@g.com", self.email_regex_for_testing))
	
	def test_camel_case_name(self):
		self.assertTrue(validator.email_validator("lAkShaY@gmail.com", self.email_regex_for_testing))

	def test_special_characters_in_domain(self):
		self.assertTrue(validator.email_validator("l.badl_ani@g_mail.com", self.email_regex_for_testing))

# Tests phone number validation thoroughly on a number of different cases and makes sure the validator returns the appropriate response based on predetermined criteria. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestPhoneNumberValidation(unittest.TestCase):
	
	phone_regex_for_testing = r'^\d{9,13}$' 

	def test_empty_string(self):
		self.assertFalse(validator.phone_number_validator("", self.phone_regex_for_testing))

	def test_only_letters_phone_number(self):
		self.assertFalse(validator.phone_number_validator("ASLBCEDGHTY", self.phone_regex_for_testing))

	def test_normal_phone_number(self):
		self.assertTrue(validator.phone_number_validator("5106924877", self.phone_regex_for_testing))

	def test_special_characters_in_phone_number(self):
		self.assertFalse(validator.phone_number_validator("510693:6;", self.phone_regex_for_testing))

	def test_only_white_space_in_phone_number(self):
		self.assertFalse(validator.phone_number_validator("      ", self.phone_regex_for_testing))
	
	def test_some_whitespace_in_phone_number(self):
		self.assertFalse(validator.phone_number_validator("5167 999990", self.phone_regex_for_testing))

	def test_too_short_phone_number(self):
		self.assertFalse(validator.phone_number_validator("516", self.phone_regex_for_testing))

	def test_too_long_phone_number(self):
		self.assertFalse(validator.phone_number_validator("513956310981432", self.phone_regex_for_testing))

	def test_no_white_space_after(self):
		self.assertFalse(validator.phone_number_validator("5106987777 ", self.phone_regex_for_testing))
	
	def test_min_length(self):
		self.assertTrue(validator.phone_number_validator("510890456", self.phone_regex_for_testing))

	def test_max_length(self):
		self.assertTrue(validator.phone_number_validator("5108904566789", self.phone_regex_for_testing))

	def test_mix_letters_numbers(self):
		self.assertFalse(validator.phone_number_validator("5169A6789", self.phone_regex_for_testing))

# Tests phone number validation thoroughly on a number of different cases and makes sure the validator returns the appropriate response based on predetermined criteria. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestEmailValidation(unittest.TestCase):
	
	address_regex_for_testing = r'(\d*)\s*(\w+)\s+((st)|(ave)|(road)|(drive)|(street)|(avenue)+),\s+(\w*),?\s*([A-Z]{2}),\s+(\d{5})$'

	def test_empty_string(self):
		self.assertFalse(validator.address_validator("", self.address_regex_for_testing))

	def test_number_needed_at_start(self):
		self.assertFalse(validator.address_validator("Suite One Telegraph Ave, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_letters_and_numbers_address(self):
		self.assertTrue(validator.address_validator("123 Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_special_characters_address(self):
		self.assertFalse(validator.address_validator("12: Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_only_white_space_in_address(self):
		self.assertFalse(validator.address_validator("      ", self.address_regex_for_testing))
	
	def test_some_extra_whitespace_in_address(self):
		self.assertFalse(validator.address_validator("123 Test  Road,  Berkeley,  CA", self.address_regex_for_testing))

	def test_too_short_address(self):
		self.assertFalse(validator.address_validator("123", self.address_regex_for_testing))

	def test_too_long_address(self):
		self.assertFalse(validator.address_validator("1231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231233123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123 Test  Road,  Berkeley,  CA", self.address_regex_for_testing))

	def test_must_end_with_zip(self):
		self.assertFalse(validator.address_validator("123 Test Road, Berkeley, CA", self.address_regex_for_testing))
	
	def test_different_street_descriptors(self):
		self.assertTrue(validator.address_validator("123 Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Drive, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Ave, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test St, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Street, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Avenue, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_no_city_name_needed(self):
		self.assertTrue(validator.address_validator("123 Test St, CA, 94704", self.address_regex_for_testing))

	def test_no_state_name_needed(self):
		self.assertTrue(validator.address_validator("123 Test St, Berkeley, 94704", self.address_regex_for_testing))

# Tests address validation thoroughly on a number of different cases and makes sure the validator returns the appropriate response based on predetermined criteria. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestAddressValidation(unittest.TestCase):
	
	address_regex_for_testing = r'(\d*)\s*(\w+)\s+((st)|(ave)|(road)|(drive)|(street)|(avenue)+),\s+(\w*),?\s*([A-Z]{2}),\s+(\d{5})$'

	def test_empty_string(self):
		self.assertFalse(validator.address_validator("", self.address_regex_for_testing))

	def test_number_needed_at_start(self):
		self.assertFalse(validator.address_validator("Suite One Telegraph Ave, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_letters_and_numbers_address(self):
		self.assertTrue(validator.address_validator("123 Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_special_characters_address(self):
		self.assertFalse(validator.address_validator("12: Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_only_white_space_in_address(self):
		self.assertFalse(validator.address_validator("      ", self.address_regex_for_testing))
	
	def test_some_extra_whitespace_in_address(self):
		self.assertFalse(validator.address_validator("123 Test  Road,  Berkeley,  CA", self.address_regex_for_testing))

	def test_too_short_address(self):
		self.assertFalse(validator.address_validator("123", self.address_regex_for_testing))

	def test_too_long_address(self):
		self.assertFalse(validator.address_validator("1231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231231233123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123 Test  Road,  Berkeley,  CA", self.address_regex_for_testing))

	def test_must_end_with_zip(self):
		self.assertFalse(validator.address_validator("123 Test Road, Berkeley, CA", self.address_regex_for_testing))
	
	def test_different_street_descriptors(self):
		self.assertTrue(validator.address_validator("123 Test Road, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Drive, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Ave, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test St, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Street, Berkeley, CA, 94704", self.address_regex_for_testing))
		self.assertTrue(validator.address_validator("123 Test Avenue, Berkeley, CA, 94704", self.address_regex_for_testing))

	def test_no_city_name_needed(self):
		self.assertTrue(validator.address_validator("123 Test St, CA, 94704", self.address_regex_for_testing))

	def test_no_state_name_needed(self):
		self.assertTrue(validator.address_validator("123 Test St, Berkeley, 94704", self.address_regex_for_testing))


# Tests logic that handles the logic behind the API calls. Tried to create a dummy elasticstore and update it with information to mimic POST, GET, PUT, DELETE requests. 
# Tried to test extremes where possible and made sure that input was sanitized appropriately to consolidate functionality of validation functions in the procedure. 
# Each function is a seperate case and is appropriately named to represent what it is trying to test.
class TestStorageAndRetrieval(unittest.TestCase):
	
		
	def test_insert_with_missing_info(self):
		self.assertEqual(logic_handler.insert_record({"name": "Lakshay Badla", "email": "l.badlani@gmail.com", "phone_number":"5189999999"}, dummy, dummy_index, debug = True), "Some information is missing in provided input")
		self.assertEqual(logic_handler.insert_record({"email": "l.badlani@gmail.com", "phone_number":"5189999999"}, dummy, dummy_index, debug = True), "Some information is missing in provided input")
		self.assertEqual(logic_handler.insert_record({"name": "Lakshay Badla", "phone_number":"5189999999"}, dummy, dummy_index, debug = True), "Some information is missing in provided input")
		self.assertEqual(logic_handler.insert_record({"name": "Lakshay Badla", "email": "l.badlani@gmail.com"}, dummy, dummy_index, debug = True), "Some information is missing in provided input")

	def test_insert_with_bad_formatted_data(self):
		self.assertEqual(logic_handler.insert_record({"name":"Laksh7y Badla", "email":"l.badlani@gmail.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA, 94704"}, dummy, dummy_index, debug = True), "Input values for Contact not formatted correctly. Please review specifications")
		self.assertEqual(logic_handler.insert_record({"name":"Lakshay Badla", "email":"l.badlani@gmail.com", "phone_number":"51A9904799", "address":"123 test ave, Berkeley, CA, 94704"}, dummy, dummy_index, debug = True), "Input values for Contact not formatted correctly. Please review specifications")
		self.assertEqual(logic_handler.insert_record({"name":"Lakshay Badla", "email":"l.badlanigmail.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA, 94704"}, dummy, dummy_index, debug = True), "Input values for Contact not formatted correctly. Please review specifications")
		self.assertEqual(logic_handler.insert_record({"name":"Lakshay Badla", "email":"l.badlani@gmail.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA"}, dummy, dummy_index, debug = True), "Input values for Contact not formatted correctly. Please review specifications")

	def test_insert_update_and_get_good_data(self):
		self.assertTrue(logic_handler.insert_record({"name":"Lakshay Badlani", "email":"l.badlani@gmail.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA, 94704"}, dummy, dummy_index, debug = True))
		self.assertTrue(logic_handler.contained("Lakshay Badlani", dummy, dummy_index))
		self.assertTrue(logic_handler.update_record(data = {"name":"Lakshay Badlani", "email":"l.badlani@yahoo.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA, 94704"}, record=logic_handler.contained("Lakshay Badlani", dummy, dummy_index), es_instance = dummy, index = dummy_index, debug = True))

	def test_update_bad_data(self):
		self.assertFalse(logic_handler.update_record({"name":"Lak78ay Badlani", "email":"l.badlani@gmail.com", "phone_number":"5109904799", "address":"123 test ave, Berkeley, CA, 94704"}, record=logic_handler.contained("Lakshay Badlani", dummy, dummy_index), es_instance= dummy, index = dummy_index, debug = True))
		self.assertFalse(logic_handler.update_record({"name":"Darcy Anderson", "email":"check1gmail.com", "phone_number":"51099A867", "address":"456 test ave, Berkeley, CA, 94704"}, record=logic_handler.contained("Lakshay Badlani", dummy, dummy_index), es_instance= dummy, index = dummy_index, debug = True))

	def search_query(self):
		self.assertTrue(logic_handler.search_query(pageSize = 1, page_offset = 0, query = { "query" : { "match_all" : {}}},  es_instance= dummy, index = dummy_index, doc_type = dummy_doc_type, debug = True))
		self.assertTrue(logic_handler.search_query(pageSize = 1, page_offset = 0, query = { "query" : {"query_string": {"default_field":"email","query":"l.badlani@gmail.com"}}},  es_instance= dummy, index = dummy_index, doc_type = dummy_doc_type, debug = True))

# Allows the unit tests to be run from the command line cleanly. 
if __name__ == '__main__':

	dummy = Elasticsearch([{'host': 'localhost', 'port': 9200}])
		
	dummy_index = "test_contact"
	dummy_doc_type = "event"

	mappings = {
	    "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
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

	if not dummy.indices.exists(dummy_index):
		dummy.indices.create(index = dummy_index, body = mappings)

	unittest.main()
