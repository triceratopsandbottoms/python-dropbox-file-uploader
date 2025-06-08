import base64
import requests
import json
from dotenv import dotenv_values

secrets = dotenv_values("../.env")

APP_KEY = secrets['DROPBOX_APP_KEY']
APP_SECRET = secrets['DROPBOX_APP_SECRET']
ACCESS_CODE_GENERATED = secrets['DROPBOX_GENERATED_ACCESS_CODE']

BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

headers = {
    'Authorization': f"Basic {BASIC_AUTH}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

response = requests.post('https://api.dropboxapi.com/oauth2/token',
                         data=data,
                         auth=(APP_KEY, APP_SECRET))
print(json.dumps(json.loads(response.text), indent=2))