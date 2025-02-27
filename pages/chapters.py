from flask import Blueprint, flash, render_template, request, redirect, send_file, session
from docx import Document

from .utils.dataset import Dataset

import pandas as pd
import os

chapters = Blueprint("chapters/", __name__, url_prefix="/chapters")

ALL_CHAPTERS = [
    {
        "index": i,
        "description": f"Description for Chapter {i}",
        "url": f'/chapters/{i}'
    } for i in range(1, 11)
]


# Till all pages are created
@chapters.route('/<int:index>')
def select_chapter_paged(index):
    return render_template('chapter.html', chapter_number=index)

@chapters.route("/")
def chapters_page():
    return render_template('all_chapters.html', chapters_list=ALL_CHAPTERS)

# Chapter 2 Page
@chapters.route('/2')
def chapter_2():
    datasets = Dataset.query.all()
    selected_dataset = session.get('selected_dataset', None)
    return render_template('chapter_2.html', datasets=datasets, selected_dataset=selected_dataset)

# Confirm Dataset for Chapter 2
@chapters.route('/<int:index>/dataset/confirm', methods=['POST'])
def confirm_dataset_for_chapter(index):
    if index != 2:
        return redirect('/chapters')
    session['selected_dataset'] = request.form.get('selected_dataset')
    return redirect('/chapters/2')

# Generate Word Document for Chapter 2 (Restored to Plain Text Paths)
@chapters.route('/<int:index>/generate/word')
def generate_word_for_chapter(index):
    selected_dataset = session.get('selected_dataset')
    if not selected_dataset:
        flash("⚠ Please select a dataset first.", "warning")
        return redirect('/chapters/2')

    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    # Duplicate 25 random rows
    duplicated_df = pd.concat([df, df.sample(25, replace=True)])
    duplicated_path = os.path.join(request.root_url, "static", "csv", f"duplicated_{selected_dataset}")
    original_path = os.path.join(request.root_url, "static", "csv", f"original_{selected_dataset}")

    duplicated_df.to_csv(duplicated_path, index=False)
    df.to_csv(original_path, index=False)

    filename = f"Chapter_{index}_Assignment.docx"

    # Create Word Document
    word_path = os.path.join("static", "generated", filename)

    doc = Document()
    doc.add_heading(f'Chapter {index} Assignment', level=1)

    # Chapter specific Document
    if index == 2:
        
        doc.add_heading('Task 1: Remove Duplicate Records', level=2)
        doc.add_paragraph("Download the dataset with duplicated rows:")

        # ✅ Plain text file paths instead of hyperlinks
        doc.add_paragraph(f"📂 Duplicated Dataset: {duplicated_path}")
        doc.add_paragraph("\n✅ Answer Key:")
        doc.add_paragraph(f"📂 Original Dataset: {original_path}")

    doc.save(word_path)

    return send_file(word_path, as_attachment=True, download_name=filename)
