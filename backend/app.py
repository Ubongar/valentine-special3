from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Validate environment variables and provide defaults
DB_USER = os.getenv("DB_USER","valentine_user")
DB_PASSWORD = os.getenv("DB_PASSWORD","securepassword")
DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to localhost if not set
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to 5432 for PostgreSQL
DB_NAME = os.getenv("DB_NAME","valentine_db")

# Check for required environment variables
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Database configuration is incomplete. Ensure all required environment variables are set.")

# PostgreSQL Database Configuration
try:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{int(DB_PORT)}/{DB_NAME}"
except ValueError:
    raise ValueError("Invalid DB_PORT value. Ensure it is a valid integer.")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define database model
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.Text, nullable=False)
    dessert = db.Column(db.Text, nullable=True)
    activities = db.Column(db.Text, nullable=True)


# Initialize the database
with app.app_context():
    db.create_all()


# API to save responses
@app.route("/save-response", methods=["POST"])
def save_response():
    data = request.get_json()
    new_response = Response(
        food=data.get("food", ""),
        dessert=data.get("dessert", ""),
        activities=data.get("activities", "")
    )
    db.session.add(new_response)
    db.session.commit()
    return jsonify({"message": "Response saved!"}), 201


# API to retrieve responses
@app.route("/get-responses", methods=["GET"])
def get_responses():
    responses = Response.query.all()
    return jsonify([
        {"id": r.id, "food": r.food, "dessert": r.dessert, "activities": r.activities}
        for r in responses
    ])


if __name__ == "__main__":
    app.run(debug=True)