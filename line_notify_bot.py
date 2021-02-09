# -*- coding: utf-8 -*-


"""line_notify_bot.py

Send messages, images, or stickers to a LINE group via LINE Notify.
This bot can't accept messages, i.e., is not interactive.
Access token can be obtrained from: https://notify-bot.line.me/ja/
Sticker and its package IDs can be chosen from: https://devdocs.line.me/files/sticker_list.pdf
https://qiita.com/moriita/items/5b199ac6b14ceaa4f7c9
"""

import requests
import pickle
import sys
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry

def pickle_dump(obj, path):
    with open(path, mode='wb') as f:
        pickle.dump(obj,f)

def pickle_load(path):
    with open(path, mode='rb') as f:
        data = pickle.load(f)
        return data

def get_html(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def add_page(name,url):
    target_url = pickle_load('./target_url.pickle')
    page_record = pickle_load('./page_record.pickle')

    target_url[name] = url
    page_record[url] = get_html(url)

    pickle_dump(target_url,'./target_url.pickle')
    pickle_dump(page_record,'./page_record.pickle')

    print(name,':',url,'\nhas added to the list')
    return 

def remove_page(name):
    target_url = pickle_load('./target_url.pickle')
    page_record = pickle_load('./page_record.pickle')

    url = target_url[name]
    del page_record[url]
    del target_url[name]

    pickle_dump(target_url,'./target_url.pickle')
    pickle_dump(page_record,'./page_record.pickle')

    print(name,'has removed from the list')
    return 



def show_list():
    target_url = pickle_load('./target_url.pickle')
    print(target_url)
    return


def main():
    
    with open('./access_token.txt') as f:
        access_token = f.read()
    
    target_url = pickle_load('./target_url.pickle')
    page_record = pickle_load('./page_record.pickle')

    bot = LINENotifyBot(access_token=access_token)
    
    for name,url in target_url.items():
        current_version_html = get_html(url)
        if current_version_html != page_record[url]:
            page_record[url] = current_version_html
            message = name+':\n'+url+'\nhas changed.'
            bot.send(message)

    print('Web page checking completed')

    pickle_dump(page_record,'./page_record.pickle')

    return


class LINENotifyBot:
    API_URL = 'https://notify-api.line.me/api/notify'
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send(
            self, message,
            image=None, sticker_package_id=None, sticker_id=None,
            ):
        payload = {
            'message': message,
            'stickerPackageId': sticker_package_id,
            'stickerId': sticker_id,
            }
        files = {}
        if image != None:
            files = {'imageFile': open(image, 'rb')}
        requests.post(
            LINENotifyBot.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
            )

if __name__ == '__main__':
    main()
