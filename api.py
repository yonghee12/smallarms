from flask import Flask
from flask import request
from flask_restful import Resource, Api
import api_func
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        # return api_func.get_descriptions(url)
        print('\n', request.args)
        urls = request.args.getlist('url')
        return api_func.get_descriptions(urls)

api.add_resource(HelloWorld, '/youtube-description')

if __name__ == '__main__':
    app.run(debug=True)