from flask import Flask, render_template, flash, redirect, request
from werkzeug.utils import secure_filename

from pages import chapters

from pages.utils.session import Session
from pages.utils.dataset import Dataset

import pandas as pd

import os

app = Flask(__name__)

Session.create(app)

app.register_blueprint(chapters)

# Home Page
@app.route('/')
def index():
    dataset_exists = Dataset.query.first() is not None
    return render_template('index.html', dataset_exists=dataset_exists)


# Upload Dataset
@app.route('/dataset/upload', methods=['POST'])
def upload_file():
    if 'dataset' not in request.files:
        flash("❌ No file selected!", "error")
        return redirect('/')

    app = Session.get_app()
    db = Session.get_database()

    file = request.files['dataset']
    if file.filename == '':
        flash("❌ No file selected!", "error")
        return redirect('/')

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Prevent duplicate uploads
        existing_dataset = Dataset.query.filter_by(filename=filename).first()
        if existing_dataset:
            flash("⚠ Dataset already exists. Please use the existing one.", "warning")
            return redirect('/')

        file.save(filepath)

        df = pd.read_csv(filepath)
        dataset_entry = Dataset(title=filename, filename=filename, data=df.to_json())
        db.session.add(dataset_entry)
        db.session.commit()

        flash("✅ Dataset uploaded successfully!", "success")
        return redirect('/')
    flash("❌ Invalid file format. Please upload a CSV file.", "error")
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
