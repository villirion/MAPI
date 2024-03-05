from flask import Flask, request
from application import List, Post, Update, Reload, Delete
from flask_cors import CORS
from handle_response import HandleResponse, HandleResponseWithBody

app = Flask(__name__)
CORS(app)

@app.route('/mapi', methods=['GET'])
def get():
    source = request.args.get('source')

    return HandleResponseWithBody(List(source), None)

@app.route('/mapi', methods=['POST'])
def post():
    data = request.json
    source = request.args.get('source')

    return HandleResponse(Post(source, data))

@app.route('/mapi', methods=['PATCH'])
def patch():
    data = request.json
    source = request.args.get('source')

    return HandleResponse(Update(source, data))

@app.route('/mapi', methods=['DELETE'])
def delete():
    data = request.json
    source = request.args.get('source')

    return HandleResponse(Delete(source, data))

@app.route('/mapi/reload', methods=['GET'])
def reload():
    source = request.args.get('source')

    Reload(source)

    return HandleResponse(None)

if __name__ == '__main__':
    app.run(debug=True)