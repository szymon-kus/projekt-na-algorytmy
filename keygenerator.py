import os
import secrets

class CryptoFileManager:
    def __init__(self, upload_folder, key_file_path):
        self.upload_folder = upload_folder
        self.key_file_path = key_file_path

        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        self.key = self.load_or_generate_key()

    def generate_key_and_save_to_file(self):
        key = secrets.token_bytes(32)

        with open(self.key_file_path, 'wb') as key_file:
            key_file.write(key)

        print("Key was generated and saved in file 'secret.key'.")
        return key

    def load_or_generate_key(self):
        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, 'rb') as key_file:
                key = key_file.read()
        else:
            key = self.generate_key_and_save_to_file()

        return key

    def xor_cipher(self, data):
        encrypted_data = bytearray()
        for byte in data:
            encrypted_data.append(byte ^ self.key[len(encrypted_data) % len(self.key)])
        return bytes(encrypted_data)