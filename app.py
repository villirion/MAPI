from flask import Flask, jsonify, request
from persistence import List, Get, Post, Update
from query import check_all_page_existence, check_all_new_chapter

app = Flask(__name__)

manhwaCSV = "manhwa.csv"
mangaCSV = "manga.csv"

@app.route('/mapi/manhwa', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def manage_manhwa():
    if request.method == 'GET':
        title = request.args.get('title')

        if title is None:
            return jsonify(List(manhwaCSV))

        result = Get(manhwaCSV, title)

        return jsonify(result[0]), result[1]

    elif request.method == 'POST':
        data = request.json

        result = Post(manhwaCSV, data)

        return jsonify(result[0]), result[1]

    elif request.method == 'PATCH':
        data = request.json

        result = Update(manhwaCSV, data)

        return jsonify(result[0]), result[1]

    elif request.method == 'DELETE':
        data = request.json

        result = Update(manhwaCSV, data)

        return jsonify(result[0]), result[1]

@app.route('/mapi/manhwa/check-url', methods=['GET'])
def check_url_manhwa():
    return jsonify(check_all_page_existence(manhwaCSV))

@app.route('/mapi/manhwa/check-new-chapter', methods=['GET'])
def check_new_chapter_manhwa():
    return jsonify(check_all_new_chapter(manhwaCSV))

if __name__ == '__main__':
    app.run(debug=True)