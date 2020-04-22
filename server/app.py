# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 

# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 

# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 

# url request handler 
class URLHandler(Resource): 

	# corresponds to the GET request. 
	# this function is called whenever there 

	# is a GET request for this resource 
	def get(self): 
		return jsonify({'response': 'endpoint to handle url'}) 

	# Corresponds to POST request 
	def post(self): 
		
		data = request.get_json()	 # status code 
		return jsonify({'url': data}), 201


# another resource to calculate the square of a number 
class FileHandler(Resource): 

	def get(self, num): 

		return jsonify({'reponse': "end point to handler urls file"}) 

    # Corresponds to POST request 
	def post(self): 
		
		data = request.get_json()	 # status code 
		return jsonify({'urls': data}), 201

# adding the defined resources along with their corresponding urls 
api.add_resource(URLHandler, '/url') 
api.add_resource(FileHandler, '/file') 


# driver function 
if __name__ == '__main__': 

	app.run(debug = True) 
