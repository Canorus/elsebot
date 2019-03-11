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
base = os.path.dirname(os.path.abspath(__file__))+'/'

with open(base+'config.json') as f:
    conf = json.load(f)

username = conf['id']
instance = conf['instance']

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
    if mode:
        try:
            newdec = json.loads(dec.replace('data: ', ''))
            type = newdec['type']
            if type == 'follow':
                new_follower = newdec['account']['id']
                followback(new_follower)
                # send mention
            elif type == 'mention':
                # analyze
                reply_to_id = newdec
        except:
            continue
    try:
        newdec = json.loads(dec.replace('data: ',''))
        if newdec['account']['bot']:
            continue
        if mode:
            type = newdec['type']
            if type == 'follow':
                new_follower = newdec['account']['id']
                followback(new_follower)
                #send into mention
            elif type == 'mention':
                # analyze
                reply_to_id = newdec['status']['id']
                reply_to_account = newdec['account']['acct']
                status = '@'+reply_to_account+' 아직 이 기능은 준비가 안 됐어요. 나중에 다시 테스트해주세요.'
                mention_to(status,reply_to_id)
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
        print('error occurred.')
        with open('error id', 'a') as fa:
            fa.write(str(newdec['status']['id'])+'\n')
        pass
