import os
import requests
import shutil
from pprint import pprint
from datetime import datetime


class USER_VK:
    def __init__(self, users_id: str, count=5, version='5.131'):
        self.url = 'https://api.vk.com/method/'
        self.users_id = users_id
        self.params = {
            'access_token': tokenVK,
            'count': count,
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
        а значение - список состоящий из кол-во лайков, дата, типоразмер и url фото"""
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
                photo_dict[str(attribute[0]) + '.jpg'] = attribute[-2:]
            else:
                photo_dict[str(attribute[0]) + '_' + str(attribute[1]) + '.jpg'] = attribute[-2:]
        return photo_dict

    def save_pc(self):
        """Функция скачивает контент на комп в папку BACKUP"""
        os.mkdir('BACKUP')
        print('Создание папки BACKUP для резервного копирования на компьютере')
        path = os.path.join(os.getcwd(), 'BACKUP')
        name_list = []
        for name, props in self._name_creating().items():
            print(f'Загрузка файла: {name}, size: {props[-2]}')
            full_path = os.path.join(path, str(name))
            name_list.append(name)
            ph = requests.get(props[-1])
            out = open(full_path, "wb")
            out.write(ph.content)
            out.close()
        return name_list


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

    def upload_files_from_a_list(self):
        name_list = unloader.save_pc()
        print('Создание папки BACKUP_UserVK на Яндекс.Диск')
        for name in name_list:
            path_to_file = os.path.join('BACKUP_UserVK', name)
            directory, file_name = path_to_file.split('\\')
            uploader._add_folder(directory)
            uploader._upload((directory + '/' + name), os.path.join('BACKUP', name))
            print(f'Выгрузка файла {name} на Яндекс.Диск')
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BACKUP')
        shutil.rmtree(path)
        print('\nУдаление папки резервного копирования с компьютера\n'
              '\n'
              'Выгрузка файлов на Яндекс.Диск завершена')


if __name__ == '__main__':

    with open('TokenVK.txt', 'r') as file:
        tokenVK = file.read().strip()

    with open('TokenYa.txt', 'r') as f:
        tokenYa = f.read().strip()

    uploader = YaUploader(tokenYa)

    unloader = USER_VK('27513')

    uploader.upload_files_from_a_list()