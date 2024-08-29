from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Swagger UI configuration
SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Path for masterblog.json in the backend directory
SWAGGER_JSON_FILE = os.path.join(os.path.dirname(__file__), 'masterblog.json')


# Serve the Swagger JSON from the backend directory
@app.route('/static/masterblog.json')
def serve_swagger_json():
    with open(SWAGGER_JSON_FILE, 'r') as f:
        return jsonify(json.load(f))


JSON_FILE = 'posts.json'


def read_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {JSON_FILE} contains invalid JSON.")
        return []


def write_posts(posts):
    with open(JSON_FILE, 'w') as f:
        json.dump(posts, f, indent=2)


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = read_posts()
    sort = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    search = request.args.get('search', '').lower()

    if sort and sort not in ['title', 'content', 'author', 'date']:
        return jsonify({"error": "Invalid sort field. Must be 'title', 'content', 'author', or 'date'."}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    sorted_posts = posts.copy()

    # Apply search filter
    if search:
        sorted_posts = [post for post in sorted_posts if
                        search in post['title'].lower() or
                        search in post['content'].lower() or
                        search in post['author'].lower() or
                        search in post['date']]

    # Apply sorting
    if sort:
        reverse = direction == 'desc'
        if sort == 'date':
            sorted_posts.sort(key=lambda x: datetime.strptime(x[sort], '%Y-%m-%d'), reverse=reverse)
        else:
            sorted_posts.sort(key=lambda x: x[sort].lower(), reverse=reverse)

    return jsonify(sorted_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json

    required_fields = ['title', 'content', 'author', 'date']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    posts = read_posts()
    new_id = max([post['id'] for post in posts], default=0) + 1

    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content'],
        "author": data['author'],
        "date": data['date']
    }

    posts.append(new_post)
    write_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    posts = read_posts()
    post = next((post for post in posts if post['id'] == id), None)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    posts = [post for post in posts if post['id'] != id]
    write_posts(posts)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.json
    posts = read_posts()
    post = next((post for post in posts if post['id'] == id), None)

    if post is None:
        return jsonify({"error": f"Post with id {id} not found"}), 404

    updatable_fields = ['title', 'content', 'author', 'date']
    for field in updatable_fields:
        if field in data:
            if field == 'date':
                try:
                    datetime.strptime(data['date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
            post[field] = data[field]

    write_posts(posts)
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('query', '').lower()
    posts = read_posts()

    matching_posts = [post for post in posts if
                      query in post['title'].lower() or
                      query in post['content'].lower() or
                      query in post['author'].lower() or
                      query in post['date']]

    return jsonify(matching_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)