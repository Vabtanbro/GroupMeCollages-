import requests
import json
from urllib.parse import unquote
import re,os

## Code To Send Message
def send_message(msg,img=None):
    headers ={}
    
    {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {"text" : msg, "bot_id" : "75b3b74cd9aa09e0b691b2954c"}
    if img:
        data = {"text" : msg, "bot_id" : "75b3b74cd9aa09e0b691b2954c","picture_url":img}
    data = json.dumps(data)
    
    response = requests.post('https://api.groupme.com/v3/bots/post', headers=headers, data=data)
    print(response.status_code)
    print(response.text)

    
## Code TO Download File From GroupMe Server
def download_file(url, local_filename='my_file.pdf'):
    response = requests.get(url)
    local_filename = ''
    if "Content-Disposition" in response.headers:
        matches = re.findall("filename\*?=['\"]?(?:UTF-\d['\"]*)?([^;\r\n\"']*)['\"]?", response.headers["Content-Disposition"])
        if not matches:
            return False,"Filename not found in Content-Disposition header."
        
        local_filename = unquote(matches[0])
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        local_filename = os.path.abspath(local_filename)
        return True,local_filename

    else:
        return False,"Content-Disposition header not found."



