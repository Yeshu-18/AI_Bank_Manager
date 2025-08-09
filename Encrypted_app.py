import os
import shutil
import re
import spacy
import getpass
from PIL import Image
import pytesseract
from cryptography.fernet import Fernet

# --- CONFIGURATION ---
DOCS_TO_PROCESS_DIR = "documents_to_process"
PROCESSED_DIR = "processed_documents"
KEY_FILE = "secret.key"

# Create directories if they don't exist
os.makedirs(DOCS_TO_PROCESS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Simple user database for authentication
USER_CREDENTIALS = {
    "admin": "pass123"
}

# --- NLP MODEL LOADING ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()
    
# --- SECURE STORAGE ENGINE ---

def generate_key():
    """Generates a new encryption key and saves it to 'secret.key'."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"\n✅ A new key has been generated and saved to '{KEY_FILE}'.")
    print("⚠️  IMPORTANT: Keep this key file safe! If you lose it, you cannot decrypt your files.")

def load_key():
    """Loads the encryption key from the 'secret.key' file."""
    if not os.path.exists(KEY_FILE):
        print("\n❌ Error: 'secret.key' not found.")
        print("Please generate a key first from the main menu.")
        return None
    return open(KEY_FILE, "rb").read()

def encrypt_file(file_path: str, key):
    """Encrypts a file using the provided key."""
    f = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            original_data = file.read()
        encrypted_data = f.encrypt(original_data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        print(f"🔒 File '{os.path.basename(file_path)}' has been securely encrypted.")
    except Exception as e:
        print(f"An error occurred during encryption: {e}")

def decrypt_file(file_path: str, key):
    """Decrypts a file using the provided key."""
    f = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"🔓 File '{os.path.basename(file_path)}' has been successfully decrypted.")
    except Exception as e:
        print(f"An error occurred during decryption. Incorrect key or corrupted file.")


# --- AI & VERIFICATION ENGINE ---

def extract_text_from_image(image_path: str) -> str:
    """Uses Tesseract OCR to extract text from an image file."""
    try:
        with Image.open(image_path) as img:
            return pytesseract.image_to_string(img)
    except FileNotFoundError:
        return None
    except Exception: # Catching specific pytesseract errors if any
        # Decrypt temporarily if the file is encrypted
        key = load_key()
        if not key: return None
        decrypt_file(image_path, key)
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
        # Re-encrypt the file immediately after reading
        encrypt_file(image_path, key)
        return text

def verify_document(text: str):
    """Uses a combination of NLP (spaCy) and Regex to find and verify document details."""
    results = {
        "doc_type": "Unknown", "name": None, "dob": None, "pan_number": None,
        "aadhaar_number": None, "verification_status": "Failed", "failure_reasons": []
    }

    # Identification and Extraction Logic... (same as before)
    if re.search(r'income tax department', text, re.IGNORECASE): results["doc_type"] = "PAN Card"
    elif re.search(r'aadhaar', text, re.IGNORECASE): results["doc_type"] = "Aadhaar Card"
    else: results["failure_reasons"].append("Could not determine document type.")
    
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not results["name"] and len(ent.text.strip().split()) > 1:
            results["name"] = ent.text.strip()
        if ent.label_ == "DATE" and not results["dob"] and re.search(r'\d{2}/\d{2}/\d{4}', ent.text):
            results["dob"] = ent.text.strip()
            
    pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', text)
    if pan_match: results["pan_number"] = pan_match.group(0)
    
    aadhaar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text)
    if aadhaar_match: results["aadhaar_number"] = aadhaar_match.group(0)

    # Verification Logic
    if results["doc_type"] == "PAN Card":
        if not results["name"]: results["failure_reasons"].append("Name not found.")
        if not results["pan_number"]: results["failure_reasons"].append("Valid PAN number not found.")
    elif results["doc_type"] == "Aadhaar Card":
        if not results["name"]: results["failure_reasons"].append("Name not found.")
        if not results["aadhaar_number"]: results["failure_reasons"].append("Valid Aadhaar number not found.")

    if not results["failure_reasons"]: results["verification_status"] = "Verified"
    return results

# --- CLI INTERFACE ---

def authenticate_user():
    """Handles user login."""
    print("--- Smart Bank AI Authentication ---")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    if USER_CREDENTIALS.get(username) == password:
        print("\n✅ Login Successful!")
        return True
    print("\n❌ Invalid credentials.")
    return False

def handle_document_processing():
    """Manages the document upload, verification, and encryption flow."""
    key = load_key()
    if not key: return

    print("\n--- Document Verification ---")
    file_name = input(f"Enter filename from '{DOCS_TO_PROCESS_DIR}' (e.g., sample_pan.png): ")
    source_path = os.path.join(DOCS_TO_PROCESS_DIR, file_name)
    
    print("\nProcessing, please wait...")
    extracted_text = extract_text_from_image(source_path)

    if extracted_text is None:
        print(f"❌ ERROR: File '{file_name}' not found.")
        return

    verification_results = verify_document(extracted_text)
    
    # Display Report... (same as before)
    print("\n--- Verification Report ---")
    print(f"Status: {'✅ Verified' if verification_results['verification_status'] == 'Verified' else '❌ Verification Failed'}")
    # ... more details can be printed here ...

    if verification_results['verification_status'] == "Verified":
        destination_path = os.path.join(PROCESSED_DIR, file_name)
        shutil.move(source_path, destination_path)
        print(f"\nMoved '{file_name}' to '{PROCESSED_DIR}'.")
        # Automatically encrypt the file after moving
        encrypt_file(destination_path, key)

def handle_decryption():
    """Handles the decryption of a specific processed file."""
    key = load_key()
    if not key: return

    print("\n--- Decrypt a Processed Document ---")
    file_name = input(f"Enter filename from '{PROCESSED_DIR}': ")
    file_path = os.path.join(PROCESSED_DIR, file_name)

    if not os.path.exists(file_path):
        print(f"❌ ERROR: File '{file_name}' not found.")
        return
        
    decrypt_file(file_path, key)


def main():
    """Main function to run the CLI application."""
    if not authenticate_user():
        return

    while True:
        print("\n--- Smart Bank Main Menu ---")
        print("1. Verify a Document")
        print("2. Decrypt a Processed Document")
        print("3. Generate/Reset Encryption Key")
        print("4. Exit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            handle_document_processing()
        elif choice == '2':
            handle_decryption()
        elif choice == '3':
            generate_key()
        elif choice == '4':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option, please try again.")

if __name__ == "__main__":
    main()
