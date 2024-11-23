from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Allowed file extensions (for simplicity, only text files in this case)
ALLOWED_EXTENSIONS = {'txt', 'csv'}

# Models
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.now())

class SensitiveData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    classification = db.Column(db.String(50), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Helper function to process sensitive data
def extract_sensitive_data(file_path):
    patterns = {
        "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
        "SSN": r"\d{3}-\d{2}-\d{4}",
        "Credit Card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    }

    classifications = {
        "PAN": "PII",  # Personally Identifiable Information
        "SSN": "PII",
        "Credit Card": "PCI",  # Payment Card Information
    }

    extracted_data = []
    with open(file_path, 'r') as file:
        for line in file:
            for data_type, pattern in patterns.items():
                matches = re.findall(pattern, line)
                for match in matches:
                    extracted_data.append({
                        "type": data_type,
                        "content": match,
                        "classification": classifications[data_type]
                    })
    return extracted_data

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check if the file type is allowed
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only text and CSV files are allowed."}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Save file metadata to the database
    new_file = File(name=file.filename)
    db.session.add(new_file)
    db.session.commit()

    # Extract sensitive data from the file
    sensitive_info = extract_sensitive_data(file_path)
    
    if not sensitive_info:
        return jsonify({
            "message": f"File '{file.filename}' uploaded but no sensitive data found.",
            "file_id": new_file.id,
            "sensitive_data": []
        }), 200

    for data in sensitive_info:
        new_sensitive_data = SensitiveData(
            type=data["type"],
            content=data["content"],
            classification=data["classification"],
            file_id=new_file.id
        )
        db.session.add(new_sensitive_data)
    db.session.commit()

    return jsonify({
        "message": f"File '{file.filename}' uploaded and processed successfully",
        "file_id": new_file.id,
        "sensitive_data": sensitive_info
    }), 200

@app.route('/files', methods=['GET'])
def list_files():
    files = File.query.all()
    result = []
    for file in files:
        sensitive_data = SensitiveData.query.filter_by(file_id=file.id).all()
        data = [({
            "type": sd.type,
            "content": sd.content,
            "classification": sd.classification
        }) for sd in sensitive_data]
        result.append({
            "file_id": file.id,
            "file_name": file.name,
            "upload_date": file.upload_date,
            "sensitive_data": data
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
