# EAI Coding Challenge 

Built a RESTful API that allows us to create contacts, get their information, update their information, delete their information, and search through a datastore specifying fields that need to match and a format relaying the start point and number of entries per page. Built using Python Flask and Elasticsearch 

### Prerequisites

Only 2 additional pieces of software need to be downloaded for this project alongside Python. They are Python Flask and ElasticSearch. To install them type the following into the terminal:

```
$ pip install flask
$ pip install elasticsearch
```

### Running the application

We need to start an instance of the Flask application (which in turn will create an elasticsearch datastore) to take advantage of the API. To do so please run the following:

```
$ export FLASK_APP=main.py
$ flask run
```

## File Structure

### Config.py 

This file contains all the admin defined settings that will customize every instance of the app and will allow certain variables to be shared over a multitude of files. It enables the user to customize the application to their liking by storing all the app defining variables. In particular it contains the vairables ELASTICSEARCH_HOST and ELASTICSEARCH_PORT, which allow the user to easily change what hostname and port the data store should run on as required by the specification. In addition it contains the ELASTICSEARCH_IDX_NAME, ELASTICSEARCH_SCHEMA, ELASTICSEARCH_DOCTYPE variables which allow the user the index name they want to store their contacts on, what type they want to classify each contact as, and the fields they want to include for each contact (I have set up to include 4 text fields by default, namely: name, address, email, and phone number). 

Moreover I have also defined strings to be used in regex functions as a way to check they meet the following criteria:

Names - No digits or special characters allowed, first name has to be included and have a length that is between 2 and 40, both the middle and last names are optional with the last name having to be between 1 and 40 characters long. The total length of the name should be between 2 and 40 characters. It should not be empty.

Emails - Allowed to be alphanumeric with certain special characters such as periods, periods, underscores, colons etc. It must contain an @ symbol and end of with a domain (which can be of any length) that includes a period i.e. .com, .edu. In addition there must be at least 1 character in between the @ symbol and the last period.

Phone Numbers - Must only contain digits and must be between 9-13 characters long. 

Addresses - Can start with either house number (as digits) or words (such as suite one), followed by a street name, comma and one of the following street indentifiers : St, Street, Ave, Avenue, Drive, Road. This should be followed by another comma, an optional town name, another comma (optional), a state code (2 capital letters only but optional), and must even with a 5 digit ZIP code with no whitespace after. This field is not case sensitive. 

### tests.py

This file contains all the tests for this project; it focuses on making sure the validation of the above mentioned fields is correct and that the logic behind storing/retrieving the data is sound. For further details please look at the comments within the file itself. 

### main.py

A placeholder file just to run the app from. 

### app/__init__.py 

This files allows us to run the Flask App and also create an instance of the elasticsearch database on the local host/port specified in the config file with the index, schema, and doctype that are set in the same file. 

### elasticsearch_helper.py

Is called by the __init__.py file, and actually calls the methods in the elasticsearch package that instantiate an object and create the index. It returns an Elasticsearch object running at the hostname/port given or renders an empty index at the name specified.

### logic_handler.py

Creates a layer of abstraction in between the REST handler and the actual storing of the information. Contains a set of functions each of which correspond to a different API call and thus each of which carry out a different operation as it interacts with the Elasticsearch datasore. This enables the aforementioned functionality to be achieved. 

### routes.py 

This file handles all the RESTful Api requests as idenitfies the method/verb type from each request and matches the url pattern the user as typed in. After indentifying the appropriate verb, it sends the data in the payload (if it exists) or the name to the appropriate function so that the request can be processed by the logic handler. It parses through the query if necessary and returns error requests if the data input is incorrect. 

### validator.py 

This file contains functions that validate each of the fields in the schema and makes sure that they conform to the specified requirements above. To do this it takes advantage of regex and other in built string requirements. It also combines all of these individual functions to check and see if a json data payload is valid. If not it returns an error message saying why it is the case otherwise it approves the data for processing (whether it be posting, updating or retreiving info).


## Running the tests

To run the tests, simple navigate to the directory with the file tests.py and run the following command: 

```
$ python tests.py
```

### Further Testing

As this is my first time working with Elasticsearch and REST Api's in general, some of the tests with regards to the storing/attaining from the database might not be as thorough as necessary. This is because I found it very difficult to maintain a dummy datastore in which the data persisted allowing for various calls from different methods. In addition pythons running of unit tests is random so it was very difficult to map the operation order. In any case, I have also tested the API using a variety of curl commands issued from the terminal. Through this method I am confident that my code functions as it should given I tried many different combinations of inputs and requests. In order to execute such commands please follow the templates below in which I have input my name and some bogus data:

#### POST /contact 
```
$ curl -d '{"name":"Lakshay Badlani", "email":"l.badlani@gmail.com", "phone_number":"5101239453", "address": "123 Test Road, Berkeley, CA, 94704"}' -H "Content-Type: application/json" -X POST http://localhost:5000/contact
```

#### GET /contact?pageSize={}&page={}&query={}
```
$ curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET ‘http://localhost:5000/contact?pageSize=4&page=1&query={“query”:{“query_string”:{“default_field”:”email”,”query”:”l.badlani@gmail.com”}}}
```

#### GET /contact/<string:name>
```
$  curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:5000/contact/Lakshay%20Badlani
```

#### PUT /contact/<string:name>
```
$ curl -X PUT -H 'Content-Type: application/json' -d '{"name": "Lakshay Badlani", "email": "l.badlani@yahoo.com", "phone_number":"5189999999", "address":"123 test avenue, berkeley, CA, 94705"}' http://127.0.0.1:5000/contact/Lakshay%20Badlani
```

#### DELETE /contact/<string:name>
```
$ curl -X DELETE -H 'Content-Type: application/json' http://127.0.0.1:5000/contact/Lakshay%20Badlani
```
