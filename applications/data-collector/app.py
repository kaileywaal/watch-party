from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configuring the database URI for SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define a model for the "Comment" table
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.String(100), nullable=False)
    video_id = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(50), nullable=False)


# Creating the table(s) in the database (if they don't already exist)
with app.app_context():
    db.create_all()


@app.route("/add_comment", methods=["POST"])
def add_comment():
    # Get data from request
    data = request.get_json()
    comment_id = data["comment_id"]
    video_id = data["video_id"]
    text = data["text"]
    author = data["author"]

    # Create a new User instance and save it to the database
    new_comment = Comment(
        comment_id=comment_id, video_id=video_id, text=text, author=author
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully"}), 201


@app.route("/comments", methods=["GET"])
def get_comments():
    comments = Comment.query.all()
    return jsonify(
        [
            {
                "id": comment.id,
                "comment_id": comment.comment_id,
                "video_id": comment.video_id,
                "text": comment.text,
                "author": comment.author,
            }
            for comment in comments
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
