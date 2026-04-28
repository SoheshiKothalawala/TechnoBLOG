from flask import Flask, request, jsonify
from flask_jwt_extended import *
from flask_cors import CORS

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret"
jwt = JWTManager(app)
CORS(app)

users = [{"username": "admin", "password": "123"}]
posts = []
post_id = 1

@app.route("/")
def home():
    return "Flask API is running"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    for u in users:
        if u["username"] == data["username"] and u["password"] == data["password"]:
            return jsonify(token=create_access_token(identity=u["username"]))
    return jsonify({"error": "Invalid"}), 401

@app.route("/posts", methods=["GET"])
def get_posts():
    return jsonify(posts[-3:])

@app.route("/create-post", methods=["POST"])
@jwt_required()
def create_post():
    global post_id
    data = request.json
    new_post = {"id": post_id, "title": data["title"], "content": data["content"], "comments": []}
    posts.append(new_post)
    post_id += 1
    return jsonify(new_post)

@app.route("/comment/<int:id>", methods=["POST"])
@jwt_required()
def comment(id):
    for p in posts:
        if p["id"] == id:
            p["comments"].append({"text": request.json["text"]})
            return jsonify(p)
    return jsonify({"error": "Not found"}), 404

app.run(debug=True)