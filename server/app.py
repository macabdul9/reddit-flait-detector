from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)

api = Api(app)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

class URLHanlder(Resource):
    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']        # vectorize the user's query and make a prediction
        
        output = {"you sent":user_query}
        return output

class FileHanlder(Resource):
    def post(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']        # vectorize the user's query and make a prediction
        
        output = {"you sent":user_query}
        return output

api.add_resource(URLHanlder, '/')
api.add_resource(FileHanlder, '/file/')
  
# example of another endpoint
# api.add_resource(PredictRatings, '/ratings')

if __name__ == '__main__':
    app.run(debug=True)