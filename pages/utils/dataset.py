from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define Dataset Model
class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)