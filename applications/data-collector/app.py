from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
# Configuring the database URI for SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Load environment variables from .env file
load_dotenv()
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


# Define a model for the "Video" table
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(100), nullable=False)


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


@app.route("/test")
def test_app():
    print("test successful")
    return "test successful"


@app.route("/add_video", methods=["POST"])
def add_video():
    """Add data for a video and its associated comments"""
    data = request.get_json()
    video_id = data["video_id"]

    new_video = Video(video_id=video_id)
    db.session.add(new_video)
    db.session.commit()

    get_comments_by_video_id(video_id)

    return jsonify({"message": "Video added successfully"}), 201


def get_comments_by_video_id(video_id):
    """Retrieve comments from a particular video by its ID"""
    url = (
        "https://www.googleapis.com/youtube/v3/commentThreads?key="
        + YOUTUBE_API_KEY
        + "&part=id,snippet&videoId="
        + video_id
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        comments = data["items"]

        for comment in comments:
            comment_id = comment["id"]
            text = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            author = comment["snippet"]["topLevelComment"]["snippet"][
                "authorDisplayName"
            ]
            success = add_comment(comment_id, video_id, text, author)
            print(success)
    else:
        # Print an error message if the request failed
        print(f"Error: {response.status_code}")


def add_comment(comment_id, video_id, text, author):
    """Add comment to database"""
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
