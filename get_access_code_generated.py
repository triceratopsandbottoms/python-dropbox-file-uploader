import webbrowser
from dotenv import dotenv_values

secrets = dotenv_values("../.env")

APP_KEY = secrets['DROPBOX_APP_KEY']
url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&' \
      f'response_type=code&token_access_type=offline'

webbrowser.open(url)