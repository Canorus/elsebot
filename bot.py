import json
import requests
import datetime
import re
from random import randint
import os
from pytz import timezone
from credential import retrieve

mode = 0
base = os.path.dirname(os.path.abspath(__file__))
with open(base+'/cred.json') as fr:
    cred = json.load(fr)

with open('config.json') as f:
    cred = json.load(f)

username = cred['id']
password = cred['pw']
instance = cred['instance']

acc = retrieve(username, instance)
head = {'Authorization':'Bearer '+acc}
uri_user = instance+'/api/v1/streaming/user'
r_user = requests.get(uri_user, header=head, stream=True)

def mention_to(content, reply_to_id, *args):
    mention = dict()
    mention['content'] = content
    mention['reply_to_id'] = reply_to_id
    mention['visibility'] = 'unlisted'
    if 'image' in args:
        u = upload_media('/home/canor/scripts/birthday_bot/image/human.jpeg')
        mention['media_ids[]']=u
    requests.post(instance+'/api/v1/statuses',header=head,data=hd)

def upload_media(media_file):
    with open(media_file, 'rb') as media:
        file_uploading = media.read()
    files = {'file':file_uploading}
    r = requests.post(instance+'/api/v1/media',headers=head,files=files)
    try:
        return r.json()['id']
    except:
        return 0

def followback(user_id):
    requests.post(instance+'/api/v1/accounts/'+user_id+'/follow',headers=head)
