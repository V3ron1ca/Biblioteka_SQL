from flask import Flask, jsonify, abort, make_response, request
from Modeles import TodosSQLite

todosSQLite = TodosSQLite()

app = Flask(__name__)
app.config["SECRET_KEY"] = "python"


@app.route("/api/v1/books/", methods=["GET"])
def books_list_api_v1():
    return jsonify(todosSQLite.all())


@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = todosSQLite.get(book_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.route("/api/v1/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todosSQLite.create(book)
    return jsonify({'book': book}), 201


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = todosSQLite.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    book = {
        'id': book_id,
        'title': data.get('title', book['title']),
        'description': data.get('description', book['description']),
        'done': data.get('done', book['done'])
    }
    todosSQLite.update(book_id, book)
    return jsonify({'book': book})


if __name__ == "__main__":
    app.run(debug=True)