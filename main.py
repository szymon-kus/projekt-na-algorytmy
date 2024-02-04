from flask import Flask, request, jsonify, send_file
import os
import base64
from managefiles import Key_Encrypt_Decrypt
import logging

#inicjalizacja flaska
app = Flask(__name__)

#Wykorzystanie klasy do stworzenia sciezki gdzie beda trzymane enkrypotwane i dekryptowane pliki oraz sciezka klucza
crypto_manager = Key_Encrypt_Decrypt(upload_folder='uploaded_files', key_file_path='secret.key')

#Endpoint do przesylania pliku i jego enkrypcji
@app.route('/upload', methods=['POST'])
def upload_file():
    #Obsluga bledow
    try:
        #Sprawdzenie czy plik zostal przesladny
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        #Sprawdzenie czy nazwa pliku jest pusta
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        original_data = file.read()
        encrypted_data = crypto_manager.encrypt(original_data)

        #Zapisanie enKryptowanego pliku na sciezce upload_folder 
        encrypted_file_path = os.path.join(crypto_manager.upload_folder, 'encrypted_' + base64.urlsafe_b64encode(file.filename.encode()).decode() + '.bin')
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        #infomacja o prawidlowym dodaniu pliku i jego enkrypcji
        return jsonify({'message': 'File uploaded and encrypted successfully'})
    
    #oblsuga bledu w przypadku przesylania pliku
    except Exception as e:
        app.logger.error(f"Error during file upload: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

#Endpoint do pobrania pliku po dekrypcji
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    #obsluga bledow
    try:
        encrypted_file_path = os.path.join(crypto_manager.upload_folder, filename)

        #Sprawdzenie czy plik istnieje
        if not os.path.exists(encrypted_file_path):
            app.logger.error(f"File not found: {filename}")
            return jsonify({'error': 'File not found'}), 404

        #Binarne odczytanie enkryptowanego pliku
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        #Dekrypcja enkryptowanego pliku
        decrypted_data = crypto_manager.decrypt(encrypted_data)

        #Zapisanie odszyfrowanego pliku na sciezce upload folder
        decrypted_file_path = os.path.join(crypto_manager.upload_folder, 'decrypted_' + filename)
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        #zworcenie odszyfrowanego pliku 
        return send_file(decrypted_file_path, as_attachment=True)
    
    #obsluga bledu podczas pobierania pliku
    except Exception as e:
        app.logger.error(f"Error during file download: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


#Uruchomienie aplikacji
if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.ERROR)

    app.run(debug=True)