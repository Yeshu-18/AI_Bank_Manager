# from flask import Flask, request, session, redirect, render_template_string
# import os

# app = Flask(__name__)
# app.secret_key = "chatbot_secret_key"  # Secret key for session management

# UPLOAD_FOLDER = 'uploaded_documents'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Define the chatbot flow with a video and hidden summarisation content
# CHATBOT_FLOW = [
#     {"type": "text", "content": "Welcome to the Education Loan Application Chatbot! Let's proceed step by step."},
#     {
#         "type": "video",
#         "content": "Please watch this introductory video before proceeding.",
#         "video_url": "/static/intro_video.mp4",
#         "summary_content": """
#         To apply for an education loan, you need to follow these steps:<br>
#         1. Check Eligibility: Secure admission to a recognized institution.<br>
#         2. Choose Loan Type: Secured (with collateral) or Unsecured (without collateral).<br>
#         3. Submit Required Documents: Identity proof, admission letter, fee structure, etc.
#         """
#     },
#     {"type": "document", "content": "Please upload your Aadhaar Card for identity and address proof."},
#     {"type": "document", "content": "Please upload your PAN Card for tax and identity verification."},
#     {"type": "document", "content": "Please upload your 10th Certificate."},
#     {"type": "document", "content": "Please upload your 12th Certificate."},
#     {"type": "optional_document", "content": "Please upload your UG Certificate if applicable. You can also skip this step."},
#     {"type": "document", "content": "Please upload your Course Fee Structure for total course fees and payment deadlines."},
#     {"type": "document", "content": "Please upload your Academic Records."},
#     {"type": "document", "content": "Please upload your Income Proof to assess your repayment capacity."},
#     {"type": "document", "content": "Please upload any Collateral Documents, if required."},
#     {"type": "text", "content": "Thank you! All steps are completed. Your application will now be processed."}
# ]

# @app.route('/', methods=['GET', 'POST'])
# def chatbot():
#     # Initialize session variables
#     if 'step' not in session:
#         session['step'] = 0

#     step = session['step']

#     # If all steps are completed
#     if step >= len(CHATBOT_FLOW):
#         session.clear()  # Clear session after completion
#         return "<h3>Thank you for using the chatbot. Your application is being processed!</h3>"

#     # Get the current step content
#     current_step = CHATBOT_FLOW[step]

#     # Handle POST request for file uploads or skipping
#     if request.method == 'POST':
#         if current_step["type"] == "document" or current_step["type"] == "optional_document":
#             if "skip" not in request.form:  # Check if the user skipped the step
#                 uploaded_file = request.files.get('document')
#                 if uploaded_file:
#                     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#                     uploaded_file.save(file_path)
#         # Move to the next step
#         session['step'] += 1
#         return redirect('/')

#     # Render the chatbot interface for the current step
#     if current_step["type"] == "text":
#         content = f"<p>{current_step['content']}</p><form method='POST'><button type='submit'>Next</button></form>"
#     elif current_step["type"] == "video":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <video width="600" controls autoplay>
#                 <source src="{current_step['video_url']}" type="video/mp4">
#                 Your browser does not support the video tag.
#             </video>
#             <div id="summary" style="display:none; margin-top: 20px;">
#                 <p>{current_step['summary_content']}</p>
#             </div>
#             <button id="toggle-summary" onclick="toggleSummary()">Summarisation</button>
#             <form method="POST">
#                 <button type='submit'>Next</button>
#             </form>
#         """
#     elif current_step["type"] == "document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document" required>
#                 <button type="submit">Upload</button>
#             </form>
#         """
#     elif current_step["type"] == "optional_document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document">
#                 <button type="submit">Upload</button>
#             </form>
#             <form method="POST">
#                 <button type="submit" name="skip" value="true">Skip</button>
#             </form>
#         """

#     # Dynamically generate and render the chatbot UI
#     return render_template_string(f"""
#         <html>
#         <head>
#             <title>Chatbot</title>
#             <script>
#                 function toggleSummary() {{
#                     var summary = document.getElementById('summary');
#                     if (summary.style.display === 'none') {{
#                         summary.style.display = 'block';
#                     }} else {{
#                         summary.style.display = 'none';
#                     }}
#                 }}
#             </script>
#         </head>
#         <body>
#             <h2>Education Loan Chatbot</h2>
#             <div style="border: 1px solid #ccc; padding: 15px; margin: 20px; border-radius: 10px;">
#                 {content}
#             </div>
#         </body>
#         </html>
#     """)

# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, session, redirect, render_template_string
# import os

# app = Flask(__name__)
# app.secret_key = "chatbot_secret_key"  # Secret key for session management

# UPLOAD_FOLDER = 'uploaded_documents'
# VIDEO_UPLOAD_FOLDER = 'uploaded_videos'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER

# # Define chatbot flow
# CHATBOT_FLOW = [
#     {"type": "text", "content": "Welcome to the Education Loan Application Chatbot! Let's proceed step by step."},
#     {"type": "video", "content": "Please watch this introductory video before proceeding.", "video_url": "/static/intro_video.mp4", "summary_content": "To apply for an education loan, you need to follow these steps:<br>1. Check Eligibility: Secure admission to a recognized institution.<br>2. Choose Loan Type: Secured (with collateral) or Unsecured (without collateral).<br>3. Submit Required Documents: Identity proof, admission letter, fee structure, etc."},
#     {"type": "document", "content": "Please upload your Aadhaar Card for identity and address proof."},
#     {"type": "document", "content": "Please upload your PAN Card for tax and identity verification."},
#     {"type": "document", "content": "Please upload your 10th Certificate."},
#     {"type": "document", "content": "Please upload your 12th Certificate."},
#     {"type": "optional_document", "content": "Please upload your UG Certificate if applicable. You can also skip this step."},
#     {"type": "document", "content": "Please upload your Course Fee Structure for total course fees and payment deadlines."},
#     {"type": "document", "content": "Please upload your Income Proof to assess your repayment capacity."},
#     {"type": "document", "content": "Please upload any Collateral Documents, if required."},
#     {"type": "video", "content": "Please record and upload a video statement confirming all documents submitted and explaining your need for the education loan."},
#     {"type": "video", "content": "Please upload a video for KYC verification, showing identity proof and confirming address details."},
#     {"type": "video", "content": "Please upload a video for Co-Applicant Declaration, where the co-applicant states their consent and financial details."},
#     {"type": "video", "content": "Please upload a video agreement, where the applicant and co-applicant verbally agree to loan terms."},
#     {"type": "video", "content": "Please upload a video disbursement request, confirming continued education and requesting the next installment."},
#     {"type": "video", "content": "Please upload an affidavit video declaring no past loan defaults and confirming provided details are accurate."},
#     {"type": "video", "content": "Please upload a collateral confirmation video showing pledged property or security."},
#     {"type": "text", "content": "Thank you! All steps are completed. Your application will now be processed."}
# ]


# @app.route('/', methods=['GET', 'POST'])
# def chatbot():
#     if 'step' not in session:
#         session['step'] = 0
#     step = session['step']

#     if step >= len(CHATBOT_FLOW):
#         session.clear()
#         return "<h3>Thank you for using the chatbot. Your application is being processed!</h3>"

#     current_step = CHATBOT_FLOW[step]
    
#     if request.method == 'POST':
#         if current_step["type"] in ["document", "optional_document"]:
#             if "skip" not in request.form:
#                 uploaded_file = request.files.get('document')
#                 if uploaded_file:
#                     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#                     uploaded_file.save(file_path)
#         elif current_step["type"] == "video" and "video_url" not in current_step:
#             if "skip" not in request.form:
#                 uploaded_video = request.files.get('video')
#                 if uploaded_video:
#                     video_path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], uploaded_video.filename)
#                     uploaded_video.save(video_path)
        
#         session['step'] += 1
#         return redirect('/')

#     if current_step["type"] == "text":
#         content = f"<p>{current_step['content']}</p><form method='POST'><button type='submit'>Next</button></form>"
#     elif current_step["type"] == "video":
#         if "video_url" in current_step:
#             content = f"""
#                 <p>{current_step['content']}</p>
#                 <video width='640' height='360' controls>
#                     <source src='{current_step['video_url']}' type='video/mp4'>
#                     Your browser does not support the video tag.
#                 </video>
#                 <div style='margin-top: 10px;'>
#                     <button id='toggle-summary' onclick='toggleSummary()'>Summarise</button>
#                     <div id='summary' style='display:none; margin-top: 10px;'>
#                         <p>{current_step['summary_content']}</p>
#                     </div>
#                 </div>
#                 <form method='POST'>
#                     <button type='submit'>Next</button>
#                 </form>
#                 <script>
#                     function toggleSummary() {{
#                         var summary = document.getElementById('summary');
#                         if (summary.style.display === 'none') {{
#                             summary.style.display = 'block';
#                         }} else {{
#                             summary.style.display = 'none';
#                         }}
#                     }}
#                 </script>
#             """
#         else:
#             content = f"""
#                 <p>{current_step['content']}</p>
#                 <form method="POST" enctype="multipart/form-data">
#                     <input type="file" name="video" accept="video/*" required>
#                     <button type="submit">Upload Video</button>
#                 </form>
#                 <form method="POST">
#                     <button type="submit" name="skip" value="true">Skip Video</button>
#                 </form>
#             """

#     elif current_step["type"] == "document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document" required>
#                 <button type="submit">Upload</button>
#             </form>
#         """
#     elif current_step["type"] == "optional_document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document">
#                 <button type="submit">Upload</button>
#             </form>
#             <form method="POST">
#                 <button type="submit" name="skip" value="true">Skip</button>
#             </form>
#         """
    
#     return render_template_string(f"""<html><head><title>Chatbot</title></head><body><h2>Education Loan Chatbot</h2><div style="border: 1px solid #ccc; padding: 15px; margin: 20px; border-radius: 10px;">{content}</div></body></html>""")

# if __name__ == '__main__':
#     app.run(debug=True)














# from flask import Flask, request, session, redirect, render_template_string
# import os
# import json
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "chatbot_secret_key"  # Secret key for session management

# UPLOAD_FOLDER = 'uploaded_documents'
# VIDEO_UPLOAD_FOLDER = 'uploaded_videos'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER

# # Define chatbot flow
# CHATBOT_FLOW = [
#     {"type": "text", "content": "Welcome to the Education Loan Application Chatbot! Let's proceed step by step."},
#     {"type": "video", "content": "Please watch this introductory video before proceeding.", "video_url": "/static/intro_video.mp4", "summary_content": "To apply for an education loan, you need to follow these steps:<br>1. Check Eligibility: Secure admission to a recognized institution.<br>2. Choose Loan Type: Secured (with collateral) or Unsecured (without collateral).<br>3. Submit Required Documents: Identity proof, admission letter, fee structure, etc."},
#     {"type": "document", "content": "Please upload your Aadhaar Card for identity and address proof."},
#     {"type": "document", "content": "Please upload your PAN Card for tax and identity verification."},
#     {"type": "document", "content": "Please upload your 10th Certificate."},
#     {"type": "document", "content": "Please upload your 12th Certificate."},
#     {"type": "optional_document", "content": "Please upload your UG Certificate if applicable. You can also skip this step."},
#     {"type": "document", "content": "Please upload your Course Fee Structure for total course fees and payment deadlines."},
#     {"type": "document", "content": "Please upload your Income Proof to assess your repayment capacity."},
#     {"type": "document", "content": "Please upload any Collateral Documents, if required."},
#     {"type": "video", "content": "Please record and upload a video statement confirming all documents submitted and explaining your need for the education loan."},
#     {"type": "video", "content": "Please upload a video for KYC verification, showing identity proof and confirming address details."},
#     {"type": "video", "content": "Please upload a video for Co-Applicant Declaration, where the co-applicant states their consent and financial details."},
#     {"type": "video", "content": "Please upload a video agreement, where the applicant and co-applicant verbally agree to loan terms."},
#     {"type": "video", "content": "Please upload a video disbursement request, confirming continued education and requesting the next installment."},
#     {"type": "video", "content": "Please upload an affidavit video declaring no past loan defaults and confirming provided details are accurate."},
#     {"type": "video", "content": "Please upload a collateral confirmation video showing pledged property or security."},
#     {"type": "text", "content": "Thank you! All steps are completed. Your application will now be processed."}
# ]

# # Helper function to save files to disk and JSON
# def save_file_to_json(file, folder, file_type):
#     file_path = os.path.join(folder, file.filename)
#     file.save(file_path)

#     # Prepare data for saving in JSON
#     file_data = {
#         'filename': file.filename,
#         'file_path': file_path,
#         'file_type': file_type,
#         'timestamp': datetime.now().isoformat()
#     }

#     # Load existing data from JSON file, if exists
#     if os.path.exists('files_data.json'):
#         with open('files_data.json', 'r') as f:
#             data = json.load(f)
#     else:
#         data = []

#     # Append the new file data
#     data.append(file_data)

#     # Save updated data back to JSON
#     with open('files_data.json', 'w') as f:
#         json.dump(data, f, indent=4)

#     return file_data

# @app.route('/', methods=['GET', 'POST'])
# def chatbot():
#     if 'step' not in session:
#         session['step'] = 0
#     step = session['step']

#     if step >= len(CHATBOT_FLOW):
#         session.clear()
#         return "<h3>Thank you for using the chatbot. Your application is being processed!</h3>"

#     current_step = CHATBOT_FLOW[step]
    
#     if request.method == 'POST':
#         if current_step["type"] in ["document", "optional_document"]:
#             if "skip" not in request.form:
#                 uploaded_file = request.files.get('document')
#                 if uploaded_file:
#                     file_data = save_file_to_json(uploaded_file, app.config['UPLOAD_FOLDER'], 'document')
#         elif current_step["type"] == "video" and "video_url" not in current_step:
#             if "skip" not in request.form:
#                 uploaded_video = request.files.get('video')
#                 if uploaded_video:
#                     video_data = save_file_to_json(uploaded_video, app.config['VIDEO_UPLOAD_FOLDER'], 'video')

#         session['step'] += 1
#         return redirect('/')

#     if current_step["type"] == "text":
#         content = f"<p>{current_step['content']}</p><form method='POST'><button type='submit'>Next</button></form>"
#     elif current_step["type"] == "video":
#         if "video_url" in current_step:
#             content = f"""
#                 <p>{current_step['content']}</p>
#                 <video width='640' height='360' controls>
#                     <source src='{current_step['video_url']}' type='video/mp4'>
#                     Your browser does not support the video tag.
#                 </video>
#                 <div style='margin-top: 10px;'>
#                     <button id='toggle-summary' onclick='toggleSummary()'>Summarise</button>
#                     <div id='summary' style='display:none; margin-top: 10px;'>
#                         <p>{current_step['summary_content']}</p>
#                     </div>
#                 </div>
#                 <form method='POST'>
#                     <button type='submit'>Next</button>
#                 </form>
#                 <script>
#                     function toggleSummary() {{
#                         var summary = document.getElementById('summary');
#                         if (summary.style.display === 'none') {{
#                             summary.style.display = 'block';
#                         }} else {{
#                             summary.style.display = 'none';
#                         }}
#                     }}
#                 </script>
#             """
#         else:
#             content = f"""
#                 <p>{current_step['content']}</p>
#                 <form method="POST" enctype="multipart/form-data">
#                     <input type="file" name="video" accept="video/*" required>
#                     <button type="submit">Upload Video</button>
#                 </form>
#                 <form method="POST">
#                     <button type="submit" name="skip" value="true">Skip Video</button>
#                 </form>
#             """
#     elif current_step["type"] == "document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document" required>
#                 <button type="submit">Upload</button>
#             </form>
#         """
#     elif current_step["type"] == "optional_document":
#         content = f"""
#             <p>{current_step['content']}</p>
#             <form method="POST" enctype="multipart/form-data">
#                 <input type="file" name="document">
#                 <button type="submit">Upload</button>
#             </form>
#             <form method="POST">
#                 <button type="submit" name="skip" value="true">Skip</button>
#             </form>
#         """
    
#     return render_template_string(f"""<html><head><title>Chatbot</title></head><body><h2>Education Loan Chatbot</h2><div style="border: 1px solid #ccc; padding: 15px; margin: 20px; border-radius: 10px;">{content}</div></body></html>""")

# if __name__ == '__main__':
#     app.run(debug=True)




    
    
# from flask import Flask, request, session, redirect, render_template_string
# import os
# import json
# import pytesseract
# from PIL import Image
# import re
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "chatbot_secret_key"

# UPLOAD_FOLDER = 'uploaded_documents'
# VIDEO_UPLOAD_FOLDER = 'uploaded_videos'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER

# def extract_text_from_image(file_path):
#     try:
#         text = pytesseract.image_to_string(Image.open(file_path))
#         return text
#     except Exception as e:
#         return "Error extracting text"

# def parse_details(document_type, text):
#     extracted_data = {}
    
#     if document_type == "Aadhaar Card":
#         extracted_data['Name'] = re.search(r'(?i)Name[:\s]+([A-Za-z ]+)', text)
#         extracted_data['DOB'] = re.search(r'\d{2}/\d{2}/\d{4}', text)
#         extracted_data['Aadhaar Number'] = re.search(r'\d{4} \d{4} \d{4}', text)
    
#     elif document_type == "PAN Card":
#         extracted_data['Name'] = re.search(r'(?i)Name[:\s]+([A-Za-z ]+)', text)
#         extracted_data['DOB'] = re.search(r'\d{2}/\d{2}/\d{4}', text)
#         extracted_data['PAN Number'] = re.search(r'[A-Z]{5}\d{4}[A-Z]', text)
    
#     elif "Certificate" in document_type:
#         extracted_data['Candidate Name'] = re.search(r'(?i)Name[:\s]+([A-Za-z ]+)', text)
#         extracted_data['Year of Passing'] = re.search(r'\b(19|20)\d{2}\b', text)
    
#     elif document_type == "Course Fee Structure":
#         extracted_data['Institution Name'] = re.search(r'(?i)Institution[:\s]+([A-Za-z ]+)', text)
#         extracted_data['Total Fees'] = re.search(r'\d{1,3}(,\d{3})*(\.\d{2})?', text)
    
#     elif document_type == "Income Proof":
#         extracted_data['Name'] = re.search(r'(?i)Name[:\s]+([A-Za-z ]+)', text)
#         extracted_data['Annual Income'] = re.search(r'\d{1,3}(,\d{3})*(\.\d{2})?', text)
    
#     return {key: match.group(1) if match else "Not found" for key, match in extracted_data.items()}

# def save_file_to_json(file, folder, file_type):
#     file_path = os.path.join(folder, file.filename)
#     file.save(file_path)
#     if file_type != "video":
#         extracted_text = extract_text_from_image(file_path)
#         extracted_data = parse_details(file_type, extracted_text)
#         session.setdefault('extracted_details', []).append({file_type: extracted_data})
#     return file_path

# @app.route('/', methods=['GET', 'POST'])
# def chatbot():
#     if 'step' not in session:
#         session['step'] = 0
#     step = session['step']
#     steps = [
#         {"type": "video", "content": "Please watch this introductory video before proceeding.", "video_url": "/static/intro_video.mp4"},
#         {"type": "document", "content": "Upload your Aadhaar Card."},
#         {"type": "document", "content": "Upload your PAN Card."},
#         {"type": "document", "content": "Upload your 10th Certificate."},
#         {"type": "document", "content": "Upload your 12th Certificate."},
#         {"type": "document", "content": "Upload your UG Certificate (if applicable)."},
#         {"type": "document", "content": "Upload your Course Fee Structure."},
#         {"type": "document", "content": "Upload your Income Proof."},
#         {"type": "document", "content": "Upload Collateral Documents, if required."},
#         {"type": "video", "content": "Upload a video statement confirming all documents submitted."}
#     ]
    
#     if step >= len(steps):
#         return render_template_string('<h3>Extracted Details:</h3><pre>{{ details }}</pre>', details=json.dumps(session.get('extracted_details', {}), indent=4))
    
#     current_step = steps[step]
    
#     if request.method == 'POST':
#         uploaded_file = request.files.get('file')
#         if uploaded_file:
#             save_file_to_json(uploaded_file, app.config['UPLOAD_FOLDER'] if current_step["type"] == "document" else app.config['VIDEO_UPLOAD_FOLDER'], current_step["type"])
#         session['step'] += 1
#         return redirect('/')
    
#     if current_step["type"] == "video" and "video_url" in current_step:
#         return render_template_string(f'<p>{current_step["content"]}</p><video width="640" height="360" controls><source src="{current_step["video_url"]}" type="video/mp4"></video><form method="POST"><button type="submit">Next</button></form>')
    
#     return render_template_string(f'<p>{current_step["content"]}</p><form method="POST" enctype="multipart/form-data"><input type="file" name="file" required><button type="submit">Upload</button></form>')

# if __name__ == '__main__':
#     app.run(debug=True)
    
    
    
    
    
    
    
    
    
    

from flask import Flask, request, session, redirect, render_template_string
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chatbot_secret_key"  # Secret key for session management

UPLOAD_FOLDER = 'uploaded_documents'
VIDEO_UPLOAD_FOLDER = 'uploaded_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER

# Define chatbot flow
CHATBOT_FLOW = [
    {"type": "text", "content": "Welcome to the Education Loan Application Chatbot! Let's proceed step by step."},
    {"type": "video", "content": "Please watch this introductory video before proceeding.", "video_url": "/static/intro_video.mp4", "summary_content": "To apply for an education loan, you need to follow these steps:<br>1. Check Eligibility: Secure admission to a recognized institution.<br>2. Choose Loan Type: Secured (with collateral) or Unsecured (without collateral).<br>3. Submit Required Documents: Identity proof, admission letter, fee structure, etc."},
    {"type": "document", "content": "Please upload your Aadhaar Card for identity and address proof."},
    {"type": "document", "content": "Please upload your PAN Card for tax and identity verification."},
    {"type": "document", "content": "Please upload your 10th Certificate."},
    {"type": "document", "content": "Please upload your 12th Certificate."},
    {"type": "optional_document", "content": "Please upload your UG Certificate if applicable. You can also skip this step."},
    {"type": "document", "content": "Please upload your Course Fee Structure for total course fees and payment deadlines."},
    {"type": "document", "content": "Please upload your Income Proof to assess your repayment capacity."},
    {"type": "document", "content": "Please upload any Collateral Documents, if required."},
    {"type": "video", "content": "Please record and upload a video statement confirming all documents submitted and explaining your need for the education loan."},
    {"type": "video", "content": "Please upload a video for KYC verification, showing identity proof and confirming address details."},
    {"type": "video", "content": "Please upload a video for Co-Applicant Declaration, where the co-applicant states their consent and financial details."},
    {"type": "video", "content": "Please upload a video agreement, where the applicant and co-applicant verbally agree to loan terms."},
    {"type": "video", "content": "Please upload a video disbursement request, confirming continued education and requesting the next installment."},
    {"type": "video", "content": "Please upload an affidavit video declaring no past loan defaults and confirming provided details are accurate."},
    {"type": "video", "content": "Please upload a collateral confirmation video showing pledged property or security."},
    {"type": "text", "content": "Thank you! All steps are completed. Your application will now be processed."}
]

# Helper function to save files to disk and JSON
import fitz  # PyMuPDF for PDFs
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text")
    return text

import pytesseract
from pdf2image import convert_from_path

# Set Tesseract path if necessary (Windows users)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(pdf_path):
    """Extracts text from scanned PDFs using OCR."""
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img) for img in images])
    return text

import re

def extract_details(text, doc_type):
    """Extracts relevant details based on document type."""
    extracted_data = {
        "Full Name": "Not Found",
        "DOB": "Not Found",
        "Gender": "Not Found",
        "Address": "Not Found",
        "Aadhaar Number": "Not Found",
        "PAN Number": "Not Found",
        "Signature": "Not Found",
        "Tax Status": "Not Found",
        "School Name": "Not Found",
        "Year of Completion": "Not Found",
        "Marks": "Not Found",
        "Degree & Major": "Not Found",
        "University Name": "Not Found",
        "CGPA/Marks": "Not Found",
        "Total Fees": "Not Found",
        "Payment Deadlines": "Not Found",
        "Course Duration": "Not Found",
        "Installment Info": "Not Found",
        "Applicant Income": "Not Found",
        "Employer Details": "Not Found",
        "Salary Slips/Tax Returns": "Not Found",
        "Co-Applicant Income": "Not Found",
        "Property Details": "Not Found",
        "Market Value": "Not Found",
        "Ownership Proof": "Not Found",
        "Legal Documents": "Not Found",
        "Mortgage Details": "Not Found"
    }

    # ✅ Initialize regex match variables to avoid UnboundLocalError
    name_match = dob_match = gender_match = address_match = aadhaar_match = None
    pan_match = signature_match = tax_status_match = school_match = year_match = marks_match = None
    degree_match = university_match = cgpa_match = fee_match = payment_match = None
    duration_match = installment_match = income_match = employer_match = salary_match = None
    co_income_match = property_match = market_value_match = ownership_match = None
    legal_docs_match = mortgage_match = None

    # ✅ Aadhaar Card Extraction
    if "Aadhaar" in doc_type:
        name_match = re.search(r"Full Name[:\s]+([\w\s]+)", text, re.IGNORECASE)
        dob_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
        gender_match = re.search(r"\b(Male|Female|Other)\b", text, re.IGNORECASE)
        address_match = re.search(r"Address[:\s]+([\w\s,]+)", text, re.IGNORECASE)
        aadhaar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text)

    # ✅ PAN Card Extraction
    elif "PAN" in doc_type:
        name_match = re.search(r"Name[:\s]+([\w\s]+)", text, re.IGNORECASE)
        dob_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
        pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
        signature_match = re.search(r"Signature[:\s]+([\w\s]+)", text, re.IGNORECASE)
        tax_status_match = re.search(r"Tax Status[:\s]+([\w\s]+)", text, re.IGNORECASE)

    # ✅ 10th & 12th Certificates Extraction
    elif "10th Certificate" in doc_type or "12th Certificate" in doc_type:
        name_match = re.search(r"Name[:\s]+([\w\s]+)", text, re.IGNORECASE)
        dob_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
        school_match = re.search(r"School[:\s]+([\w\s]+)", text, re.IGNORECASE)
        year_match = re.search(r"Year of Completion[:\s]+(\d{4})", text)
        marks_match = re.search(r"Marks[:\s]+([\d./]+)", text)

    # ✅ UG Certificate Extraction
    elif "UG Certificate" in doc_type:
        name_match = re.search(r"Name[:\s]+([\w\s]+)", text, re.IGNORECASE)
        degree_match = re.search(r"Degree[:\s]+([\w\s]+)", text, re.IGNORECASE)
        university_match = re.search(r"University[:\s]+([\w\s]+)", text, re.IGNORECASE)
        year_match = re.search(r"Year of Completion[:\s]+(\d{4})", text)
        cgpa_match = re.search(r"CGPA[:\s]+([\d./]+)", text)

    # ✅ Course Fee Structure Extraction
    elif "Course Fee Structure" in doc_type:
        fee_match = re.search(r"(Total Fees|Fees Payable)[:\s]+([\d,]+)", text, re.IGNORECASE)
        payment_match = re.search(r"(Payment Due Date|Payment Deadlines)[:\s]+([\w\s,]+)", text, re.IGNORECASE)
        duration_match = re.search(r"(Course Duration|Program Length)[:\s]+([\w\s]+)", text, re.IGNORECASE)
        installment_match = re.search(r"(Installment Amount|Installment Info)[:\s]+([\w\s,]+)", text, re.IGNORECASE)

        print("\n🛠 Extracted Course Fee Structure Info:")  # ✅ Debugging
        print("Total Fees:", fee_match.group(2) if fee_match else "Not Found")
        print("Payment Deadlines:", payment_match.group(2) if payment_match else "Not Found")
        print("Course Duration:", duration_match.group(2) if duration_match else "Not Found")
        print("Installments:", installment_match.group(2) if installment_match else "Not Found")


    # ✅ Income Proof Extraction
    elif "Income Proof" in doc_type:
        income_match = re.search(r"Applicant Income[:\s]+([\d,]+)", text, re.IGNORECASE)
        employer_match = re.search(r"Employer[:\s]+([\w\s]+)", text, re.IGNORECASE)
        salary_match = re.search(r"Salary[:\s]+([\d,]+)", text, re.IGNORECASE)
        co_income_match = re.search(r"Co-Applicant Income[:\s]+([\d,]+)", text, re.IGNORECASE)

    # ✅ Collateral Documents Extraction
    elif "Collateral" in doc_type:
        property_match = re.search(r"Property Details[:\s]+([\w\s,]+)", text, re.IGNORECASE)
        market_value_match = re.search(r"Market Value[:\s]+([\d,]+)", text, re.IGNORECASE)
        ownership_match = re.search(r"Ownership Proof[:\s]+([\w\s,]+)", text, re.IGNORECASE)
        legal_docs_match = re.search(r"Legal Documents[:\s]+([\w\s,]+)", text, re.IGNORECASE)
        mortgage_match = re.search(r"Mortgage[:\s]+([\w\s,]+)", text, re.IGNORECASE)

    # ✅ Assign extracted values only if match is found
    extracted_data["Full Name"] = name_match.group(1).strip() if name_match else "Not Found"
    extracted_data["DOB"] = dob_match.group(1).strip() if dob_match else "Not Found"
    extracted_data["Gender"] = gender_match.group(1).strip() if gender_match else "Not Found"
    extracted_data["Address"] = address_match.group(1).strip() if address_match else "Not Found"
    extracted_data["Aadhaar Number"] = aadhaar_match.group(0).strip() if aadhaar_match else "Not Found"
    extracted_data["PAN Number"] = pan_match.group(0).strip() if pan_match else "Not Found"
    extracted_data["Signature"] = signature_match.group(1).strip() if signature_match else "Not Found"
    extracted_data["Tax Status"] = tax_status_match.group(1).strip() if tax_status_match else "Not Found"
    extracted_data["School Name"] = school_match.group(1).strip() if school_match else "Not Found"
    extracted_data["Year of Completion"] = year_match.group(1).strip() if year_match else "Not Found"
    extracted_data["Marks"] = marks_match.group(1).strip() if marks_match else "Not Found"
    extracted_data["Degree & Major"] = degree_match.group(1).strip() if degree_match else "Not Found"
    extracted_data["University Name"] = university_match.group(1).strip() if university_match else "Not Found"
    extracted_data["CGPA/Marks"] = cgpa_match.group(1).strip() if cgpa_match else "Not Found"

    # ✅ Course Fee Structure Extraction
    extracted_data["Total Fees"] = fee_match.group(2).strip() if fee_match else "Not Found"
    extracted_data["Payment Deadlines"] = payment_match.group(2).strip() if payment_match else "Not Found"
    extracted_data["Course Duration"] = duration_match.group(2).strip() if duration_match else "Not Found"
    extracted_data["Installment Info"] = installment_match.group(2).strip() if installment_match else "Not Found"

    # ✅ Income Proof Extraction
    extracted_data["Applicant Income"] = income_match.group(1).strip() if income_match else "Not Found"
    extracted_data["Employer Details"] = employer_match.group(1).strip() if employer_match else "Not Found"
    extracted_data["Salary Slips/Tax Returns"] = salary_match.group(1).strip() if salary_match else "Not Found"
    extracted_data["Co-Applicant Income"] = co_income_match.group(1).strip() if co_income_match else "Not Found"

    # ✅ Collateral Documents Extraction
    extracted_data["Property Details"] = property_match.group(1).strip() if property_match else "Not Found"
    extracted_data["Market Value"] = market_value_match.group(1).strip() if market_value_match else "Not Found"
    extracted_data["Ownership Proof"] = ownership_match.group(1).strip() if ownership_match else "Not Found"
    extracted_data["Legal Documents"] = legal_docs_match.group(1).strip() if legal_docs_match else "Not Found"
    extracted_data["Mortgage Details"] = mortgage_match.group(1).strip() if mortgage_match else "Not Found"


    return extracted_data



def save_file_to_json(file, folder, file_type, doc_type):
    """Saves file and extracts data (handles OCR for scanned documents)."""
    file_path = os.path.join(folder, file.filename)
    file.save(file_path)

    # ✅ Detect if the PDF is scanned and apply OCR
    extracted_text = extract_text_from_pdf(file_path)
    if len(extracted_text.strip()) < 10:  # If text extraction fails, use OCR
        extracted_text = extract_text_with_ocr(file_path)

    print("\n🔍 Extracted Text from PDF (Before Regex):\n", extracted_text)  # ✅ Debugging
    print("📌 Detected Document Type:", doc_type)  # ✅ Debugging

    extracted_data = extract_details(extracted_text, doc_type)

    file_data = {
        'filename': file.filename,
        'file_path': file_path,
        'file_type': file_type,
        'doc_type': doc_type,
        'timestamp': datetime.now().isoformat(),
        'extracted_data': extracted_data
    }

    return file_data


@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if 'step' not in session:
        session['step'] = 0
        session.pop("extracted_data", None)

    step = session['step']

    # If all steps are completed, automatically restart the process
    if step >= len(CHATBOT_FLOW):
        session.clear()  # Clear session to restart the process
        return redirect('/')  # Redirect to the first step

    # Current step based on the flow
    current_step = CHATBOT_FLOW[step]
    extracted_data = session.get("extracted_data", {})  # Retrieve stored extracted data

    content = ""  # Initialize content to avoid UnboundLocalError
    show_next_button = False  # Initially hide the "Next" button
    video_preview_url = None  # Initialize video preview URL to None

    # Step Type Handling
    if current_step["type"] == "text":
        content = f"<p>{current_step['content']}</p>"

    elif current_step["type"] == "video":
        content = f"""
            <p>{current_step['content']}</p>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="video" accept="video/*" required>
                <button type="submit">Upload Video</button>
            </form>
        """
        if video_preview_url:
            content += f"""
                <h3>Video Preview:</h3>
                <video width="320" height="240" controls>
                    <source src="{video_preview_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            """

    elif current_step["type"] in ["document", "optional_document"]:
        content = f"""
            <p>{current_step['content']}</p>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="document" required>
                <button type="submit">Upload</button>
            </form>
        """
        if current_step["type"] == "optional_document":
            content += """
                <form method="POST">
                    <button type="submit" name="skip" value="true">Skip</button>
                </form>
            """

    # Handling form submissions
    if request.method == 'POST':
        if "next" in request.form:  # Move to next step only when "Next" is clicked
            session['step'] += 1  # Increment step
            session.pop("extracted_data", None)  # Clear extracted data after proceeding
            return redirect('/')  # Redirect to the next page

        if current_step["type"] in ["document", "optional_document"]:
            if "skip" in request.form:  # Handle skipping UG Certificate
                session['step'] += 1
                return redirect('/')

            uploaded_file = request.files.get('document')
            if uploaded_file:
                doc_type = current_step["content"].replace("Please upload your ", "").split(" for")[0].strip(".")
                print(f"\n📌 Detected Document Type: {doc_type}")  # Debugging

                file_data = save_file_to_json(uploaded_file, UPLOAD_FOLDER, 'document', doc_type)

                # Preserve previous extracted data instead of overwriting
                extracted_data.update(file_data.get("extracted_data", {}))
                session["extracted_data"] = extracted_data  # Store in session

                show_next_button = True  # Show "Next" button after upload

        elif current_step["type"] == "video":
            uploaded_video = request.files.get('video')
            if uploaded_video:
                video_file_path = os.path.join(VIDEO_UPLOAD_FOLDER, uploaded_video.filename)
                uploaded_video.save(video_file_path)

                # Set the video preview URL to the saved file path
                video_preview_url = f"/uploads/videos/{uploaded_video.filename}"
                show_next_button = True  # Show "Next" button after video upload

    # Display only found extracted details (hide "Not Found" values)
    if extracted_data:
        content += "<h3>Extracted Details:</h3><ul>"
        for key, value in extracted_data.items():
            if value and value != "Not Found":
                content += f"<li><strong>{key}:</strong> {value}</li>"
        content += "</ul>"

    # Show "Next" button only on the first page and after file/video upload
    if show_next_button or step == 0:
        content += """
            <form method="POST">
                <button type="submit" name="next" value="true">Next</button>
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
