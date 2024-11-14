from flask import Flask, render_template, request, redirect, url_for
import difflib
import os
import pdfplumber
from docx import Document

UPLOAD_FOLDER = './uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    if 'file1' not in request.files or 'file2' not in request.files:
        return redirect(url_for('index'))

    file1 = request.files['file1']
    file2 = request.files['file2']

    # Save files temporarily for reading
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
    file1.save(file1_path)
    file2.save(file2_path)

    # Check file type and read content accordingly
    file1_text = ''
    file2_text = ''

    if file1.filename.endswith('.pdf'):
        file1_text = read_pdf(file1_path)
    elif file1.filename.endswith('.docx'):
        file1_text = read_docx(file1_path)

    if file2.filename.endswith('.pdf'):
        file2_text = read_pdf(file2_path)
    elif file2.filename.endswith('.docx'):
        file2_text = read_docx(file2_path)

    # Compare using difflib
    d = difflib.Differ()
    diff = list(d.compare(file1_text.splitlines(), file2_text.splitlines()))
    print(diff)

    # Clean up the saved files
    os.remove(file1_path)
    os.remove(file2_path)

    return render_template('index.html', diff=diff)

if __name__ == '__main__':
    app.run(debug=True, port=2323)
