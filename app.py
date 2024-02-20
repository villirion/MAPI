from flask import Flask, request
from persistence import List, Post, Update, Reload, Delete
from flask_cors import CORS
from handle_response import HandleResponse, HandleResponseWithBody

app = Flask(__name__)
CORS(app)

manhwaCSV = "P:\\CSV\\manhwa.csv"
Reload(manhwaCSV)

@app.route('/mapi/manhwa', methods=['GET'])
def get_manhwa():
    return HandleResponseWithBody(List(manhwaCSV), None)

@app.route('/mapi/manhwa', methods=['POST'])
def post_manhwa():
    data = request.json
    return HandleResponse(Post(manhwaCSV, data))

@app.route('/mapi/manhwa', methods=['PATCH'])
def patch_manhwa():
    data = request.json
    return HandleResponse(Update(manhwaCSV, data))

@app.route('/mapi/manhwa', methods=['DELETE'])
def delete_manhwa():
    data = request.json
    return HandleResponse(Delete(manhwaCSV, data))

@app.route('/mapi/manhwa/reload', methods=['GET'])
def reload_manhwa():
    Reload(manhwaCSV)
    return HandleResponse(None)


if __name__ == '__main__':
    app.run(debug=True)