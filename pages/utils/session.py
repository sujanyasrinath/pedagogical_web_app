from .dataset import db

import os

class Session:
    instance = None

    def __init__(self, app):
        self.app = app
        self.db = db

        self.app.config['UPLOAD_FOLDER'] = 'static/uploads'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datasets.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.secret_key = "supersecretkey"
        
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()

        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    @staticmethod
    def create(app):
        Session.instance = Session(app)
    
    @staticmethod
    def get_app():
        return Session.instance.app
    
    @staticmethod
    def get_database():
        return Session.instance.db
