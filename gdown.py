from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import argparse
import subprocess
import json
from tld import get_tld
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import requests

# bot settings
BOT_TOKEN = '6130808120:AAHkDLbYWLFs0f4-EHwpejkVOHXH-ux-j3o'
CHAT_ID = '1970794348'


# command parser
parser = argparse.ArgumentParser(description='google rive upload and download')
parser.add_argument("-l", "--links", help="Prints the supplied argument.", nargs='*')
args = parser.parse_args()
# args = ["https://drive.google.com/file/d/=1AdAr9-iMYD4wd-N-nzU8bcIs0ss5LnSC"]

# gdrive settings
scope = ["https://www.googleapis.com/auth/drive"]
gauth = GoogleAuth()
gauth.auth_method = 'service'
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
drive = GoogleDrive(gauth)

# bot message
MESSAGE = "Screenshot 👉\nPixeldrain 👇👇👇👇\n480p👉 480_r\n720p👉 720_r\n1080p👉 1080_r\n-----------------------------\n\nOffical Site 👇👇👇👇\n480p👉 480p_r\n720p👉 720p_r\n1080p👉 1080p_r\n\nPASSWORD 👉 https://t.me/c/1227529573/1207"
all_link = {}



# making message without domain
def handle_domain(string: str):
    string = string.replace('-', ' ').split(' ')
    message = '' 
    for word in string:
        if '.' in word:
            try:
                get_tld(word, fix_protocol=True)
            except:
                message += word + ' '
        else:
            message += word + ' '
    if message.strip().replace('  ', ' ').endswith('.mkv') or message.strip().replace('  ', ' ').endswith('.mp4'):
        message2 = message.strip().replace('.mkv', '').replace('.mp4', '').split(' ')[-1]
        if '.' in message2:
            return message.strip().replace(message2, ' ').replace('  ', ' ').replace('  ', ' ').strip()
        else:
           return message.strip().replace('  ', ' ').strip()
    else:
        return message.strip().replace('  ', ' ') + '.mkv'



# loop for handling update and function for message

def send_message(bot_token, chat_id, message):
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'disable_web_page_preview': True}
    response = requests.post(send_message_url, data=data)
    return response

remember = {}
for arg in args.links:
    link = arg.split('=')[1]
    try:
        file = drive.CreateFile({'id': link})
        name = file['title']
        name = handle_domain(name)
        print("Downloading", name)
        file.GetContentFile(name, acknowledge_abuse=True)
        print("Uploading pixeldrain", name)
        server = requests.get("https://api.gofile.io/getServer")
        server = server.json()["data"]["server"]
        files = {'file': open(name, 'rb'),
                'token': (None, 'nrjNg7USiVmujjHkXYlDq9RYOvAnDL7S'),
                }
        pixeldrain = requests.post(f'https://{server}.gofile.io/uploadFile', files=files)
        pixel_link = pixeldrain.json()["data"]["downloadPage"]
        print("Uploading gdrive", name)
        onedrive = subprocess.check_output(['rclone', 'copy', name, 'one:Public/2023/Feb/' + date.today().strftime('%d')])
        # onedrive
        # pixel_link
        # print(pixel_link)
        
        if name[:6].lower().strip() in remember.keys():
            remember[name[:6].lower().strip()]
            all_link[name[:6].lower().strip()] = remember[name[:6].lower().strip()]
        else:
            all_link[name[:6].lower().strip()] = MESSAGE
            remember[name[:6].lower().strip()] = MESSAGE
        # if '480p' in name:
        #     all_links[name[:6]][480] = data
        # elif '720p' in name:
        #     all_links[name[:6]][720] = data
        # elif '1080p' in name:
        #     all_links[name[:6]][1080] = data
        # try:
        if '480p' in name:
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('480_r', f'{pixel_link}')
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('480p_r', 'https://allinonepaid.vercel.app/Public/2023/Feb/'+date.today().strftime('%d')+'/'+name.replace(' ', '%20'))
        if '720p' in name:
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('720_r', f'{pixel_link}')
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('720p_r', 'https://allinonepaid.vercel.app/Public/2023/Feb/'+date.today().strftime('%d')+'/'+name.replace(' ', '%20'))
        if '1080p' in name:
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('1080_r', f'{pixel_link}')
            all_link[name[:6].lower().strip()] = all_link[name[:6].lower().strip()].replace('1080p_r', 'https://allinonepaid.vercel.app/Public/2023/Feb/'+date.today().strftime('%d')+'/'+name.replace(' ', '%20'))
    except Exception as e:
        print(e)
    try:
        remember[name[:6].lower().strip()] = all_link[name[:6].lower().strip()]
        all_link[name[:6].lower().strip()]
    except:
        pass

try:
    for name, link in all_link.items():
        new_message = link.replace('480_r', ' ').replace('720_r', ' ').replace('1080_r', ' ').replace('480p_r', ' ').replace('720p_r', ' ').replace('1080p_r', ' ')
        send_message(BOT_TOKEN, CHAT_ID, name)
        send_message(BOT_TOKEN, CHAT_ID, new_message)
except:
    pass
