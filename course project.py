## V Выгрузка из ВК: создает словарь {id: [likes, date, type, url} из самых больших фоток. !!! Исправлены ошибки
#  V Формирование имени будущего файла из кол-ва лайков. Если количество лайков повторяется, к значению likes добавляется дата.
#  V Создание папки для резервного копирования на компе и загрузка в нее файлов
## Выгрузка на Яндекс Диск: Основа есть, но пока не знаю, как по урлам туда загружать
# Удаление папки резервного копирования с компа
# Разобраться с requirements и прогресс-бар(что такое, впервые слышу...)

import os
import requests
import shutil
from pprint import pprint
from datetime import datetime


with open('TokenVK.txt', 'r') as file:
    tokenVK = file.read().strip()

with open('TokenYa.txt', 'r') as f:
    tokenYa = f.read().strip()


class USER_VK:
    def __init__(self, users_id: str, version='5.131'):
        self.url = 'https://api.vk.com/method/'
        self.users_id = users_id
        self.params = {
            'access_token': tokenVK,
            'v': version
        }

    def _get_photo_to_unload_vk(self):
        """Функция выдает данные по фото альбому пользователя ввиде json"""
        unload_url = self.url + 'photos.get'
        params = {
            'owner_id': self.users_id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(unload_url, params={**self.params, **params})
        return response.json()

    def _sort_ph(self):
        """отбор фоток по размеру. Фиксация количества лайков.
        На выходе словарь, где ключ - ID,
        а значение - список состоящий из кол-во лайков, дата, типоразмера и url фото"""
        sizes_dict = {}
        for album in self._get_photo_to_unload_vk()['response']['items']:
            likes = str(album['likes']['count'])
            d = str(datetime.fromtimestamp(album['date']))
            date = d[:10]
            id = album['id']
            size_max = 0
            for s in album['sizes']:
                if size_max <= s['height'] * s['width']:
                    size_max = s['height'] * s['width']
                    sizes_dict[id] = [likes, date, s['type'], s['url']]
        return sizes_dict

    def _name_creating(self):
        photo_dict = {}
        for attribute in self._sort_ph().values():
            if str(attribute[0]) + '.jpg' not in photo_dict.keys():
                photo_dict[str(attribute[0]) + '.jpg'] = attribute[-1:]
            else:
                photo_dict[str(attribute[0]) + '_' + str(attribute[1]) + '.jpg'] = attribute[-1:]
        return photo_dict

    def save_pc(self):
        """Функция скачивает контент на комп в папку BACKUP"""
        os.mkdir('BACKUP')
        path = os.path.join(os.getcwd(), 'BACKUP')
        for name, props in self._name_creating().items():
            full_path = os.path.join(path, str(name))
            print(full_path)
            ph = requests.get(props[-1])
            out = open(full_path, "wb")
            out.write(ph.content)
            out.close()


# Формирование выходных данных как в задании ?????????????????
    def regrouping(self):
        favorits = []
        for k, v in self.sort_ph().items():
           favorits.append({'file_name': k, 'sizes': v[-2]})
        return favorits



# class YaUploader:
#     def __init__(self, token: str):
#         self.token = tokenYa
#         self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
#
#     def _get_headers(self):
#         return {
#             'Content-Type': 'application/json',
#             'Authorization': f'OAuth {self.token}'
#         }
#
#     def _get_upload_link(self, file_path):
#         upload_url = self.url + 'upload'
#         headers = self._get_headers()
#         params = {'path': file_path, 'overwrite': 'true'}
#         response = requests.get(upload_url, headers=headers, params=params)
#         return response.json()
#
#     def _add_folder(self, path):
#         headers = self._get_headers()
#         requests.put(f'{self.url}?path={path}', headers=headers)
#
#     def _upload(self, file_path, path_to_file):
#         link_dict = self._get_upload_link(file_path=file_path)
#         href = link_dict['href']
#         response = requests.put(href, data=open(path_to_file, 'rb'))
#         response.raise_for_status()
#         if response.status_code == 201:
#             print('Success')
#
#     def upload_files_from_a_list(self, path_to_file_list):
#         for path_to_file in path_to_file_list:
#             directory, file_name = path_to_file.split('/')
#             uploader._add_folder(directory)
#             uploader._upload(path_to_file, path_to_file)
#

unloader = USER_VK('1')

unloader.save_pc()


# uploader = YaUploader(tokenYa)
# uploader._add_folder('Course_Project')
# path_to_file_list = ['Course_Project/https://sun9-west.userapi.com/sun9-6/s/v1/if1/1OCyHTvNRzj8B1BRF1l9o034d1XEZNWuhwVvPePqAk7ksfrWa_Yj-TnmBRPXCuT8trNdAw.jpg?size=908x1080&quality=96&type=album']
#
