from flask import Flask, request, jsonify, send_file
from cryptography.fernet import Fernet
import os
import base64

def generate_key_and_save_to_file():

    key = Fernet.generate_key()

    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

    print("Klucz został wygenerowany i zapisany do pliku 'secret.key'.")

if __name__ == "__main__":
    generate_key_and_save_to_file()

app = Flask(__name__)

key_file_path = 'secret.key'


def load_or_generate_key():
    if os.path.exists(key_file_path):
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
    return key

upload_folder = 'uploaded_files'

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

key = load_or_generate_key()
cipher_suite = Fernet(key)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400


        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)


        with open(file_path, 'rb') as original_file:
            original_data = original_file.read()
            encrypted_data = cipher_suite.encrypt(original_data)


        encrypted_file_path = os.path.join(upload_folder, 'encrypted_' + base64.urlsafe_b64encode(file.filename.encode()).decode() + '.bin')
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        return jsonify({'message': 'File uploaded and encrypted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        encrypted_file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(encrypted_file_path):
            return jsonify({'error': 'File not found'}), 404

        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)


        decrypted_file_path = os.path.join(upload_folder, 'decrypted_' + filename)
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)



        return send_file(decrypted_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    finally:
        if 'decrypted_file_path' in locals() and os.path.exists(decrypted_file_path):
            os.remove(decrypted_file_path)    

if __name__ == '__main__':
    app.run(debug=True)