from app import db, Dataset, app

with app.app_context():  # ✅ Create an application context
    datasets = Dataset.query.all()

    # Use a set to track unique filenames
    seen_files = set()
    for dataset in datasets:
        if dataset.filename in seen_files:
            db.session.delete(dataset)  # Remove duplicates
        else:
            seen_files.add(dataset.filename)

    # Commit the deletion
    db.session.commit()
    print("✅ Duplicate datasets removed!")
