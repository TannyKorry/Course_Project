# with open('tokenVK.txt', 'r') as file:
#     tokenVK = file.read().strip()
#
#
# with open('tokenYa.txt', 'r') as file:
#     tokenYa = file.read().strip()
# #     print(tokenYa)

import time
import requests
from pprint import pprint

# URL = 'https://api.vk.com/method/users.get'
# params = {
#     'user_ids': '27513',
#     'access_token': tokenVK,
#     'v':'5.131',
#     'fields': 'photo_100'
# }
# res = requests.get(URL, params=params)
# pprint(res.json())

# выгрузка инфы
url = 'https://api.vk.com/method/photos.get'
params = {
    'access_token': tokenVK,
    'v': '5.131',
    'users_id': '27513',
    'owner_id': '486158475',
    'album_id': 'profile',
    'extended': '1'
    }
response = requests.get(url, params=params)
req = response.json()
# отбор фоток по размеру. Фиксация количества лайков
# pprint(req['response']['items'])
for album in req['response']['items']:
    data = album['date']
    likes = album['likes']['count']

    sizes_max = 0
    for s in album['sizes']:
        sizes = s['height'] * s['width']
        url_p = s['url']

        if sizes > sizes_max:
            sizes_max = sizes
            url_photo = url_p
    pprint(likes)
    pprint(url_p)

class YaUploader:
    def __init__(self, token: str):
        self.token = tokenYa
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, file_path):
        upload_url = self.url + 'upload'
        headers = self._get_headers()
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def _add_folder(self, path):
        headers = self._get_headers()
        requests.put(f'{self.url}?path={path}', headers=headers)

        def _upload(self, file_path, path_to_file):
            link_dict = self._get_upload_link(file_path=file_path)
            href = link_dict['href']
            response = requests.put(href, data=open(path_to_file, 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')

        def upload_files_from_a_list(self, path_to_file_list):
            for path_to_file in path_to_file_list:
                directory, file_name = path_to_file.split('/')
                uploader._add_folder(directory)
                uploader._upload(path_to_file, path_to_file)

    if __name__ == '__main__':
        with open('ТокенYa.txt', 'r') as f:
            token = f.read().strip()
        with open('tokenVK.txt', 'r') as file:
            tokenVK = file.read().strip()

        uploader = YaUploader(token)

        path_to_file_list = ['Course_Project/' + 'url_p']

        uploader.upload_files_from_a_list(path_to_file_list)