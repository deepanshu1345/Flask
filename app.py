from flask import Flask, render_template, request, redirect, url_for, flash
import difflib
import os
import tempfile
import pdfplumber
from docx import Document
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def read_pdf(file_path):
    """Read content from a PDF file using pdfplumber."""
    with pdfplumber.open(file_path) as pdf:
        content = []
        for page in pdf.pages:
            content.append(page.extract_text())
        return '\n'.join(content)

def read_docx(file_path):
    """Read content from a DOCX file using python-docx."""
    doc = Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return '\n'.join(content)

def read_txt(file_path):
    """Read content from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST','GET'])
def compare():
    if 'file1' not in request.files or 'file2' not in request.files:
        flash("Please upload both files.")
        return redirect(url_for('index'))

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == file2.filename:
        flash("Error: Both files have the same name and extension. Please upload different files.")
        return redirect(url_for('index'))

    # Create unique file paths in a temporary directory
    temp_dir = tempfile.gettempdir()
    file1_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file1.filename}")
    file2_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file2.filename}")

    # Save files temporarily for reading
    file1.save(file1_path)
    file2.save(file2_path)

    # Check file type and read content accordingly
    file1_text = ''
    file2_text = ''

    # File 1 content reading based on extension
    if file1.filename.endswith('.pdf'):
        file1_text = read_pdf(file1_path)
    elif file1.filename.endswith('.docx'):
        file1_text = read_docx(file1_path)
    elif file1.filename.endswith('.txt'):
        file1_text = read_txt(file1_path)
    else:
        flash("File 1 is not a supported format. Only PDF, DOCX, and TXT are allowed.")
        os.remove(file1_path)
        os.remove(file2_path)
        return redirect(url_for('index'))

    # File 2 content reading based on extension
    if file2.filename.endswith('.pdf'):
        file2_text = read_pdf(file2_path)
    elif file2.filename.endswith('.docx'):
        file2_text = read_docx(file2_path)
    elif file2.filename.endswith('.txt'):
        file2_text = read_txt(file2_path)
    else:
        flash("File 2 is not a supported format. Only PDF, DOCX, and TXT are allowed.")
        os.remove(file1_path)
        os.remove(file2_path)
        return redirect(url_for('index'))

    # Compare using difflib
    d = difflib.Differ()
    diff = list(d.compare(file1_text.splitlines(), file2_text.splitlines()))

    # Clean up the saved files
    try:
        os.remove(file1_path)
        os.remove(file2_path)
    except Exception as e:
        print(f"Error deleting files: {e}")

    return render_template('index.html', diff=diff)

if __name__ == '__main__':
    app.run(debug=True, port=2323)
