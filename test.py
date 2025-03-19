from flask import Flask, request, session, redirect, render_template_string
import os
import json
import pytesseract
import cv2
import re
import pdfplumber
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chatbot_secret_key"  # Secret key for session management

UPLOAD_FOLDER = 'uploaded_documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chatbot Flow Definition
CHATBOT_FLOW = [
    {"type": "text", "content": "Welcome to the Education Loan Application Chatbot!"},
    {"type": "document", "content": "Please upload your Aadhaar Card for identity verification."},
    {"type": "text", "content": "Thank you! Your application will be processed."}
]

# Function to Extract Aadhaar Details
def extract_aadhaar_details(file_path):
    text = ""

    # Extract text from PDF
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + " "
    else:
        # Extract text from Image
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

    # Remove unnecessary newlines
    text = text.replace("\n", " ")

    # Aadhaar Number Extraction
    aadhaar_match = re.search(r'Aadhaar Number:\s*(\d{4} \d{4} \d{4})', text)

    # Full Name Extraction (Stopping at "DOB" to prevent extra capture)
    full_name_match = re.search(r'Full Name:\s*([A-Za-z ]+)(?=\s*DOB:)', text)

    # Date of Birth Extraction
    dob_match = re.search(r'DOB:\s*(\d{2}/\d{2}/\d{4}|\d{4})', text)

    # Gender Extraction
    gender_match = re.search(r'Gender:\s*(Male|Female)', text)

    # Address Extraction (Stopping at "Aadhaar Number" to prevent extra text)
    address_match = re.search(r'Address:\s*(.*?)(?=\s*Aadhaar Number:)', text)

    extracted_data = {
        "Full Name": full_name_match.group(1).strip() if full_name_match else "Not Found",
        "DOB": dob_match.group(1) if dob_match else "Not Found",
        "Gender": gender_match.group(1) if gender_match else "Not Found",
        "Aadhaar Number": aadhaar_match.group(1) if aadhaar_match else "Not Found",
        "Address": address_match.group(1).strip() if address_match else "Not Found"
    }

    return extracted_data


# Handle File Upload and Extraction
@app.route('/upload_aadhaar', methods=['POST'])
def upload_aadhaar():
    if 'document' not in request.files:
        return "No file uploaded", 400

    file = request.files['document']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract Aadhaar Details
    extracted_data = extract_aadhaar_details(file_path)

    # Save to JSON
    with open('extracted_data.json', 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    return f"Extracted Aadhaar Details: {json.dumps(extracted_data, indent=4)}"

# Chatbot Flow Handling
@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if 'step' not in session:
        session['step'] = 0
    step = session['step']

    if step >= len(CHATBOT_FLOW):
        session.clear()
        return "<h3>Thank you for using the chatbot. Your application is being processed!</h3>"

    current_step = CHATBOT_FLOW[step]

    if request.method == 'POST':
        if current_step["type"] == "document":
            uploaded_file = request.files.get('document')
            if uploaded_file:
                return redirect('/upload_aadhaar')

        session['step'] += 1
        return redirect('/')

    if current_step["type"] == "text":
        content = f"<p>{current_step['content']}</p><form method='POST'><button type='submit'>Next</button></form>"
    elif current_step["type"] == "document":
        content = f"""
            <p>{current_step['content']}</p>
            <form action="/upload_aadhaar" method="POST" enctype="multipart/form-data">
                <input type="file" name="document" required>
                <button type="submit">Upload</button>
            </form>
        """
    
    return render_template_string(f"""
        <html>
        <head><title>Chatbot</title></head>
        <body>
            <h2>Education Loan Chatbot</h2>
            <div style="border: 1px solid #ccc; padding: 15px; margin: 20px; border-radius: 10px;">
                {content}
            </div>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
