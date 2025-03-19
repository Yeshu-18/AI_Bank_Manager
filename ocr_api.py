from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'processed_documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def process_document():
    if 'document' not in request.files:
        return jsonify({"error": "No document uploaded"}), 400
    
    file = request.files['document']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Perform OCR
    image = Image.open(file_path)
    extracted_text = pytesseract.image_to_string(image)

    # Dummy extraction logic (Replace with NLP models if needed)
    key_details = {
        "name": "Extracted Name Placeholder",
        "dob": "01-01-1990",
        "income": "50000",
        "employment_type": "Salaried"
    }

    return jsonify({"extracted_text": extracted_text, "key_details": key_details})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # OCR API runs on port 5000
