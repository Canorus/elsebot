import json
import requests
import datetime
import re
from random import randint
import os
from pytz import timezone
from credential import retrieve
from konlpy.tag import Kkma
from bs4 import BeautifulSoup as bs

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
r_user = requests.get(uri_user, headers=head, stream=True)
print('connected to stream')

def mention_to(content, reply_to_id, *args):
    mention = dict()
    mention['status'] = content
    mention['reply_to_id'] = reply_to_id
    mention['visibility'] = 'unlisted'
    if 'image' in args:
        u = upload_media('/home/canor/scripts/birthday_bot/image/human.jpeg')
        mention['media_ids[]']=u
    requests.post(instance+'/api/v1/statuses',headers=head,data=mention)

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
    print('requesting followback')
    requests.post(instance+'/api/v1/accounts/'+user_id+'/follow',headers=head)

for l in r_user.iter_lines():
    is_not_mention = 1
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
        for i in newdec:
            print(str(i)+': '+str(newdec[i]))
        print('------------------------------')
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
                print('mention coming in')
                reply_to_id = newdec['id']
                reply_to_account = newdec['account']['acct']
                status = '@'+reply_to_account+' 아직 이 기능은 준비가 안 됐어요. 나중에 다시 테스트해주세요.'
                mention_to(status,reply_to_id)
                is_not_mention = 0
            try:
                type = newdec['type']
            except:
                pass
        else:
            status = bs(str(newdec['content']),'html.parser').get_text()
            if '자 ' in status:
                continue
            if ('자','VV') in kkma.pos(status) and is_not_mention:
                print(status)
                reply_to_id = newdec['id']
                reply_to_account = newdec['account']['acct']
                if newdec['account']['display_name']:
                    username = newdec['account']['display_name']
                else:
                    username = newdec['account']['username']
                status = '@'+reply_to_account+' 좋은 꿈 꾸세요'
                mention_to(status, reply_to_id)
    except:
        print('error occurred.')
