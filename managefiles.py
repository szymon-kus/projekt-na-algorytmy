import os
from cryptography.fernet import Fernet

#Storzenie klasy do generacji klucza, enkryptowania pliku i jego dekryptowania
class Key_Encrypt_Decrypt:
    def __init__(self, upload_folder, key_file_path):
        self.upload_folder = upload_folder
        self.key_file_path = key_file_path

        #Sprawdzenie czy istnieje folder z plikami
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        self.key = self.load_or_generate_key()

    #Tworzenie klucza z biblioteka Fernet crypotgrpahy (klucz symetryczny)
    def generate_key_and_save_to_file(self):
        key = Fernet.generate_key()

        with open(self.key_file_path, 'wb') as key_file:
            key_file.write(key)

        print("Key was generated and saved in file 'secret.key'.")
        return key

    #Sprawdzenie czy klucz juz istnieje
    def load_or_generate_key(self):
        if os.path.exists(self.key_file_path):
            with open(self.key_file_path, 'rb') as key_file:
                key = key_file.read()
        else:
            key = self.generate_key_and_save_to_file()

        return key

    #Enkryptowanie pliku
    def encrypt(self, file_to_encrypt):
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(file_to_encrypt)
        return encrypted_data

    #Dekrypcja pliku
    def decrypt(self, file_to_decrypt):
        cipher = Fernet(self.key)
        decrypted_data = cipher.decrypt(file_to_decrypt)
        return decrypted_data