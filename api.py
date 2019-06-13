from flask import Flask
from flask_restful import Resource, Api
import api_func

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, url):
        return api_func.get_descriptions(url)

api.add_resource(HelloWorld, '/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)