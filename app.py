from flask import Flask, jsonify, request
from persistence import List, Get, Post, Update, Reload, Delete
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

manhwaCSV = "P:\CSV\manhwa.csv"
Reload(manhwaCSV)

@app.route('/mapi/manhwa', methods=['GET'])
def get_manhwa():
    title = request.args.get('title')

    if title is None:
        return jsonify(List(manhwaCSV))

    result = Get(manhwaCSV, title)

    return jsonify(result[0]), result[1]

@app.route('/mapi/manhwa', methods=['POST'])
def post_manhwa():
    data = request.json
    result = Post(manhwaCSV, data)
    return jsonify(result[0]), result[1]

@app.route('/mapi/manhwa', methods=['PATCH'])
def patch_manhwa():
    data = request.json
    result = Update(manhwaCSV, data)
    return jsonify(result[0]), result[1]

@app.route('/mapi/manhwa', methods=['DELETE'])
def delete_manhwa():
    data = request.json
    result = Delete(manhwaCSV, data)
    return jsonify(result[0]), result[1]

if __name__ == '__main__':
    app.run(debug=True)