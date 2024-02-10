from .utils import send_message,download_file
from .models import StudentTb
import requests
import csv,json



from django.conf import settings
access_token = settings.ACCESS_TOKEN


def load_student(data):
    file_id     = data.get('attachments',[])[0]['file_id']
    group_id    = data.get('group_id','')
    url = 'https://file.groupme.com/v1/{}/files/{}?access_token={}&omit-content-disposition=false'.format(group_id,file_id,access_token)
    status,msg = download_file(url=url)
    print(status,msg,"file download status")
    if status :
        with open(msg, 'r') as file:
            reader = csv.DictReader(file)                
            for row in reader:
                print(row)
                uid = row.pop('uid', None)                    
                # Update or create the student based on the 'uid'
                student, created = StudentTb.objects.update_or_create(uid=uid,defaults=row)
                print(f"{created=}")
        return msg
    else :
    
        return  False


def create_group(grp_name="testGrp"):
    

    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
    }

    params = {
        'token': access_token,
    }

    json_data = {
        'name':grp_name,
        "share": True,
    }

    response = requests.post('https://api.groupme.com/v3/groups', params=params, headers=headers, json=json_data)
    print(response.text)
    json_data =json.loads(response.text)
    share_url = json_data['response']['share_url'] 
    return share_url




def load_grp_his(group_id):
    url      = f"https://api.groupme.com/v3/groups/{group_id}/messages?token={access_token}"
    response = requests.get(url)
    messages = json.loads(response.text)['response']['messages']

    message_array = []

    with open("chat_history.txt","a",encoding="utf-8") as out_file:
        for message in messages[::-1]:
            msg = f"{message['name']} : {message['text']}\n"
            print(msg)
            message_array.append(msg)
            out_file.write(msg)
    return message_array

print(load_grp_his(99214826))
