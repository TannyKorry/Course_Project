## V Выгрузка из ВК: создает словарь {like: type: url} из самых больших фоток.
#  V Когда количество лайков повторяется  к ключу like добавляется дата.
## Выгрузка на Яндекс Диск: Основа есть, но пока не знаю, как по урлам туда загружать
# Разобраться с requirements и прогресс-бар(что такое, впервые слышу...)

import requests
from pprint import pprint
from datetime import datetime

with open('TokenVK.txt', 'r') as file:
    tokenVK = file.read().strip()


class USER_VK:
    def __init__(self, users_id: str, version='5.131'):
        self.url = 'https://api.vk.com/method/'
        self.users_id = users_id
        self.params = {
            'access_token': tokenVK,
            'v': version
        }

    def get_photo_to_unload_vk(self):
        """Функция выдает данные по фото альбому пользователя ввиде json"""
        unload_url = self.url + 'photos.get'
        params = {
            'owner_id': self.users_id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(unload_url, params={**self.params, **params})
        res = response.json()
        return res

    def sort_ph(self):
        """отбор фоток по размеру. Фиксация количества лайков.
        На выходе словарь, где ключ - это кол-во лайков,
        а значение - список состоящий из url-фото и даты"""
        photo_dict, sizes_dict = {}, {}
        for album in self.get_photo_to_unload_vk()['response']['items']:
            likes = album['likes']['count']
            date = datetime.fromtimestamp(album['date'])
            for s in album['sizes']:
                sizes_dict[s['type']] = [s['height'] * s['width'], s['type'], s['url']]
            if likes not in photo_dict.keys():
                photo_dict[likes] = max(sizes_dict.values())
            else:
                photo_dict[str(likes) + '_' + str(date)] = max(sizes_dict.values())
        return photo_dict


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

    # def upload_files_from_a_list(self, directory):
    #     uploader._add_folder(directory)
    #     for l, u in unloader.sort_ph().items():
    #         # print(l)
    #         print(uploader._upload('directory'+'/'+'l'+'.jpg', l))

with open('TokenYa.txt', 'r') as f:
    tokenYa = f.read().strip()

unloader = USER_VK('27513')
pprint(unloader.sort_ph())
uploader = YaUploader(tokenYa)
# uploader._add_folder('Course_Project')
# path_to_file_list = ['Course_Project/https://sun9-west.userapi.com/sun9-6/s/v1/if1/1OCyHTvNRzj8B1BRF1l9o034d1XEZNWuhwVvPePqAk7ksfrWa_Yj-TnmBRPXCuT8trNdAw.jpg?size=908x1080&quality=96&type=album']
#
# uploader.upload_files_from_a_list(path_to_file_list)