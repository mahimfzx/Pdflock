from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/lockpdf', methods=['POST'])
def lock_pdf():
    password = request.form.get('password')
    pdf_file = request.files.get('file')
    if not pdf_file or not password:
        return {"error": "PDF file and password are required"}, 400
    
    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    
    pdf_writer.encrypt(password)
    
    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    
    return send_file(output_stream, attachment_filename='locked.pdf', as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
