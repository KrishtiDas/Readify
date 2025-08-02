import os
from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        file = request.files['pdf']
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            reader = PdfReader(filepath)
            extracted_text = ''
            for page in reader.pages:
                extracted_text += page.extract_text() or ''

    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
