from flask import Blueprint, flash, render_template, request, redirect, send_file, session
from docx import Document

from docx.shared import Inches
from .utils.dataset import Dataset

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import io
import base64
from io import StringIO

def save_plot_image(plot_func, filename, df_column, **kwargs):
    """Helper function to generate a plot and save it as an image file."""
    fig, ax = plt.subplots(figsize=(6, 4))
    plot_func(data=df_column, ax=ax, **kwargs)  # ✅ Pass ax as keyword argument
    
    img_path = os.path.join("static", "plots", filename)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)  # Ensure directory exists
    plt.savefig(img_path, format="png", bbox_inches="tight")
    plt.close(fig)

    return img_path

chapters = Blueprint("chapters/", __name__, url_prefix="/chapters")

ALL_CHAPTERS = [
    {
        "index": i,
        "description": f"Description for Chapter {i}",
        "url": f'/chapters/{i}'
    } for i in range(1, 11)
]

def create_chapter_1_document(doc, selected_dataset, chapter_1_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_heading(chapter_1_details['question'])
    if show_answer:
        doc.add_paragraph('THIS IS AN ANSWER KEY')
    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_2_document(doc, selected_dataset, chapter_2_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    # Duplicate 25 random rows
    duplicated_df = pd.concat([df, df.sample(25, replace=True)])
    duplicated_path = os.path.join(request.root_url, "static", "csv", f"duplicated_{selected_dataset}")
    original_path = os.path.join(request.root_url, "static", "csv", f"original_{selected_dataset}")

    duplicated_df.to_csv(duplicated_path, index=False)
    df.to_csv(original_path, index=False)

    doc.add_heading('Task 1: Remove Duplicate Records', level=2)
    doc.add_paragraph("Download the dataset with duplicated rows:")

    # ✅ Plain text file paths instead of hyperlinks
    doc.add_paragraph(f"📂 Duplicated Dataset: {duplicated_path}")
    doc.add_paragraph("\n✅ Answer Key:")
    doc.add_paragraph(f"📂 Original Dataset: {original_path}")

def create_chapter_3_document(doc, selected_dataset, chapter_3_details, show_answer=False):
    """Generates a Word document for Chapter 3 with visualizations."""

    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(StringIO(dataset.data))  # ✅ FIX: Read JSON correctly

    doc.add_heading('Chapter 3: Making Sense through Data Visualization', level=1)
    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

    # Data Summary
    doc.add_heading('Data Summary', level=2)
    doc.add_paragraph(str(df.describe()))

    # Select the first numeric column for visualization
    numeric_columns = df.select_dtypes(include=['number']).columns
    if numeric_columns.empty:
        doc.add_paragraph("No numeric columns available for visualization.")
        return

    selected_column = numeric_columns[0]  # Use the first numeric column
    doc.add_paragraph(f"Visualizing Column: {selected_column}")

    # Generate and insert plots
    hist_img = save_plot_image(sns.histplot, "histogram.png", df[selected_column], bins=10, kde=True, color="blue")
    doc.add_heading('Histogram', level=2)
    doc.add_picture(hist_img, width=Inches(4.5))

    box_img = save_plot_image(sns.boxplot, "boxplot.png", df[selected_column], color="red")
    doc.add_heading('Box Plot', level=2)
    doc.add_picture(box_img, width=Inches(4.5))

    density_img = save_plot_image(sns.kdeplot, "densityplot.png", df[selected_column], fill=True, color="green")
    doc.add_heading('Density Plot', level=2)
    doc.add_picture(density_img, width=Inches(4.5))

    # Show Answer Key
    if show_answer:
        doc.add_page_break()
        doc.add_heading("Answer Key", level=1)
        doc.add_paragraph("This section contains the cleaned dataset after removing invalid/missing entries.")

        # Handle missing values
        cleaned_df = df.dropna()
        doc.add_paragraph(f"Number of rows before cleaning: {len(df)}")
        doc.add_paragraph(f"Number of rows after cleaning: {len(cleaned_df)}")

        # Export cleaned dataset
        cleaned_path = os.path.join("static", "csv", f"cleaned_{selected_dataset}")
        os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)  # Ensure directory exists
        cleaned_df.to_csv(cleaned_path, index=False)
        doc.add_paragraph(f"📂 Cleaned Dataset: {cleaned_path}")



def create_chapter_4_document(doc, selected_dataset, chapter_4_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_5_document(doc, selected_dataset, chapter_5_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_6_document(doc, selected_dataset, chapter_6_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_7_document(doc, selected_dataset, chapter_7_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_8_document(doc, selected_dataset, chapter_8_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_9_document(doc, selected_dataset, chapter_9_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

def create_chapter_10_document(doc, selected_dataset, chapter_10_details, show_answer=False):
    dataset = Dataset.query.filter_by(filename=selected_dataset).first()
    df = pd.read_json(dataset.data)

    doc.add_paragraph(f'Selected Dataset: {selected_dataset}')

DOCUMENT_ACTIONS = {
    1: {
        'session_keys': ['selected_dataset', 'chapter_1_details'],
        'action': create_chapter_1_document
    },
    2: {
        'session_keys': ['selected_dataset', 'chapter_2_details'],
        'action': create_chapter_2_document
    },
    3: {
        'session_keys': ['selected_dataset', 'chapter_3_details'],
        'action': create_chapter_3_document
    },
    4: {
        'session_keys': ['selected_dataset', 'chapter_4_details'],
        'action': create_chapter_4_document
    },
    5: {
        'session_keys': ['selected_dataset', 'chapter_5_details'],
        'action': create_chapter_5_document
    },
    6: {
        'session_keys': ['selected_dataset', 'chapter_6_details'],
        'action': create_chapter_6_document
    },
    7: {
        'session_keys': ['selected_dataset', 'chapter_7_details'],
        'action': create_chapter_7_document
    },
    8: {
        'session_keys': ['selected_dataset', 'chapter_8_details'],
        'action': create_chapter_8_document
    },
    9: {
        'session_keys': ['selected_dataset', 'chapter_9_details'],
        'action': create_chapter_9_document
    },
    10: {
        'session_keys': ['selected_dataset', 'chapter_10_details'],
        'action': create_chapter_10_document
    },
}

@chapters.route("/")
def chapters_page():
    session['selected_dataset'] = None
    return render_template('all_chapters.html', chapters_list=ALL_CHAPTERS)


def get_context(chapter, actions_complete=False):
    return {
        'meta': {
            'datasets': Dataset.query.all(),
            'selected_dataset': session.get('selected_dataset', None),
            'chapter_number': chapter,
            'actions_complete': actions_complete
        }
    }


# Chapter 1 Page
@chapters.route('/1', methods=['GET', 'POST'])
def chapter_1():
    chapter_number = 1
    actions_complete = False
    if request.method == 'POST':
        session['chapter_1_details'] = request.form
        actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_1.html', **context)

# Chapter 2 Page
@chapters.route('/2')
def chapter_2():
    chapter_number = 2
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_2.html', **context)

# Chapter 3 Page
@chapters.route('/3')
def chapter_3():
    chapter_number = 3
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_3.html', **context)

# Chapter 4 Page
@chapters.route('/4')
def chapter_4():
    chapter_number = 4
    actions_complete = False
    if request.method == 'POST':
        session['chapter_4_details'] = request.form
        actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_4.html', **context)

# Chapter 5 Page
@chapters.route('/5')
def chapter_5():
    chapter_number = 5
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_5.html', **context)

# Chapter 6 Page
@chapters.route('/6')
def chapter_6():
    chapter_number = 6
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_6.html', **context)

# Chapter 7 Page
@chapters.route('/7')
def chapter_7():
    chapter_number = 7
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_7.html', **context)

# Chapter 8 Page
@chapters.route('/8')
def chapter_8():
    chapter_number = 8
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_8.html', **context)

# Chapter 9 Page
@chapters.route('/9')
def chapter_9():
    chapter_number = 9
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_9.html', **context)

# Chapter 10 Page
@chapters.route('/10')
def chapter_10():
    chapter_number = 10
    actions_complete = True
    context = get_context(chapter_number, actions_complete)
    return render_template('chapter_10.html', **context)

# Confirm Dataset for Chapter 2
@chapters.route('/<int:index>/dataset/confirm', methods=['POST'])
def confirm_dataset_for_chapter(index):
    session['selected_dataset'] = request.form.get('selected_dataset')
    return redirect(f'/chapters/{index}')

# Generate Word Document for Chapter 2 (Restored to Plain Text Paths)
@chapters.route('/<int:index>/generate/word/<string:q_key>')
def generate_word_for_chapter(index, q_key):
    selected_dataset = session.get('selected_dataset')
    procedure = DOCUMENT_ACTIONS.get(index)
    if not selected_dataset:
        flash("⚠ Please select a dataset first.", "warning")
        return redirect(f'/chapters/{index}')
    if not procedure:
        return redirect(f'/chapters/{index}')

    filename = f"Chapter_{index}_Assignment_{q_key.capitalize()}.docx"

    # Create Word Document
    word_path = os.path.join("static", "generated", filename)

    doc = Document()
    doc.add_heading(f'Chapter {index} Assignment', level=1)

    props = {
        "show_answer": q_key == 'answer'
    }
    for key in procedure.get('session_keys', []):
        props[key] = session.get(key)
    print(procedure, props)
    procedure['action'](doc, **props)

    doc.save(word_path)

    return send_file(word_path, as_attachment=True, download_name=filename)
