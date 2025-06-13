import os
import dropbox
import requests
import configparser
from dotenv import dotenv_values

# load secrets from file
secrets = dotenv_values("../.env")

credentials_dir = secrets['DROPBOXUPLOADER_CREDENTIALS_DIR']

class DropboxHandler:
    def __init__(self):
        # Configuration parameters
        self.source_directory = ""
        self.local_file_path = 'file.txt'
        self.credentials_directory = credentials_dir
        self.dropbox_directory = ""
        # Initialize Dropbox API with access token
        self.access_token = self.read_credentials_value("Authentication", "access_token")
        self.dbx = dropbox.Dropbox(self.access_token)

    def read_credentials_value(self, section, key):
        # Read a value from the credentials file
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)

        try:
            return config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"read_credentials_value function: Error reading config value: {e}")
            return None

    def update_credentials_key_value(self, section, key, value):
        # Update a key-value pair in the credentials file
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)
        config.set(section, key, value)

        with open(self.credentials_directory, 'w') as config_file:
            config.write(config_file)
            print(f"Key '{key}' value updated successfully in section '{section}'")

    def generate_new_access_token(self, app_key, app_secret, refresh_token):
        # Generate a new access token using the provided credentials
        url = "https://api.dropbox.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": app_key,
            "client_secret": app_secret,
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print("generate_new_access_token function: Failed to get a new access token.")
            print(f"generate_new_access_token function: Status code: {response.status_code}")
            print(f"generate_new_access_token function: Response: {response.text}")
            return None

    def check_token_validity(self):
        # Check if the existing token is still valid
        try: 
            self.dbx.files_list_folder('')
            #print("Token is valid")
        except dropbox.exceptions.AuthError:
            #print("Token is expired, generating new access token ...")
            app_key = self.read_credentials_value("Authentication", "app_key")
            app_secret = self.read_credentials_value("Authentication", "app_secret")
            refresh_token = self.read_credentials_value("Authentication", "refresh_token")
            new_token = self.generate_new_access_token(app_key, app_secret, refresh_token)

            if new_token:
                self.update_credentials_key_value("Authentication", "access_token", new_token)
                self.access_token = new_token
                self.dbx = dropbox.Dropbox(self.access_token)
        except dropbox.exceptions.DropboxException as e:
            print("check_token_validity function: An error occurred while checking the token:", e)

    def upload_files(self, file, saveAs):
        # Upload a file to Dropbox
        try:
            self.check_token_validity()
            #file_name = os.path.basename(self.local_file_path)

            #with open(self.local_file_path, "rb") as file:
            self.dbx.files_upload(file, f"{self.dropbox_directory}/{saveAs}", mode=dropbox.files.WriteMode("overwrite"))
            #print(f"File '{saveAs}' uploaded successfully to Dropbox.")

        except Exception as e:
            print(f"upload_files function: An error occurred while saving {saveAs}:", e)
            
    def download_files(self, db_file_path, local_file_path):
        # Download a file from Dropbox
        try:
            self.check_token_validity()

            self.dbx.files_download_to_file(local_file_path, f"{self.dropbox_directory}/{db_file_path}")
            print(f"File '{db_file_path}' downloaded successfully to '{local_file_path}'.")

        except Exception as e:
            print(f"upload_files function: An error occurred while saving {local_file_path}:", e)

# def main():
    # # Main program flow
    # print("Start uploading files ...")
    # dropbox_uploader = DropboxUploader()
    # dropbox_uploader.upload_files('muss das wirklich sein', 'text.txt')
    # print("End uploading files")

# if __name__ == "__main__":
    # main()
