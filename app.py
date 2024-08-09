from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import docx
import PyPDF2
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords




app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_keywords(text):
    tokens = word_tokenize(text)
    keywords = [word for word, pos in pos_tag(tokens) if pos.startswith('NN') and word.lower() not in stopwords.words('english')]
    return keywords





def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    keywords = extract_keywords(text)
    return text, keywords


def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extract_text()
    keywords = extract_keywords(text)
    return text, keywords

def extract_text(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return 'No file part'
    
    file = request.files['resume']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        text, keywords = extract_text(file_path)
        # Process the extracted text (e.g., store it in a database)
        os.remove(file_path)  
        return 'Resume uploaded and processed successfully'

if __name__ == '__main__':
    app.run(debug=True)
