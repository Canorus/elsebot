import json
import requests
import datetime
import re
from random import randint
import os
from pytz import timezone
from credential import retrieve
from konlpy.tag import Kkma

kkma = Kkma()
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

for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    if dec == 'event: notification':
        mode = 1
    elif dec == 'event: update':
        mode = 0
    elif dec == ':thump':
        mode = 0
        continue
    try:
        newdec = json.loads(dec.replace('data: ',''))
        if newdec['account']['bot']:
            continue
        try:
            type = newdec['type']
        except:
            pass
        if ('자','VV') in kkma.pos(newdec['status']):
            reply_to_id = newdec['status']['id']
            reply_to_account = newdec['account']['acct']
            if newdec['account']['display_name']:
                username = newdec['account']['display_name']
            else:
                username = newdec['account']['username']
            status = '@'+reply_to_account+' 좋은 꿈 꾸세요'
            mention_to(status, reply_to_id)
    except:
        pass
