from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SensitiveData(db.Model):
    __tablename__ = 'sensitive_data'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    classification = db.Column(db.String(50), nullable=True)  # Add this column
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)

class File(db.Model):
    __tablename__ = 'file'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sensitive_data = db.relationship('SensitiveData', backref='file', lazy=True)
