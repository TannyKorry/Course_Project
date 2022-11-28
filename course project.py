import configparser
import requests
from pprint import pprint
from datetime import datetime


class USER_VK:
    def __init__(self, users_id: str, album_id, count=5, version='5.131'):
        self.url = 'https://api.vk.com/method/'
        self.users_id = users_id
        self.params = {
            'access_token': tokenVK,
            'album_id': album_id,
            'count': count,
            'v': version
        }

    def _screenName_id_definition(self):
        """Функция определяет ID пользователя по screen-name"""
        unload_url = self.url + 'users.get'
        params = {
            'user_ids': self.users_id
        }
        res = requests.get(unload_url, params={**self.params, **params}).json()
        for us in res['response']:
            us['id']
        return us['id']

    def _get_photo_to_unload_vk(self):
        """Функция выдает данные по фото альбому пользователя в виде json"""
        unload_url = self.url + 'photos.get'
        params = {
            'owner_id': self._screenName_id_definition(),
            'extended': '1'
        }
        response = requests.get(unload_url, params={**self.params, **params}).json()
        return response

    def _sort_ph(self):
        """Отбор фоток по размеру. Фиксация количества лайков.
        На выходе словарь, где ключ - ID,
        а значение - список состоящий из кол-ва лайков, даты, типоразмера и url фото"""
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


class YaUploader:
    def __init__(self, token: str):
        self.token = tokenYa
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _add_folder(self, path):
        headers = self._get_headers()
        params = {'overwrite': 'true'}
        requests.put(f'{self.url}?path={path}', headers=headers, params=params)

    def _upload(self, file_path, path_to_file):
        headers = self._get_headers()
        params = {'path': file_path, 'url': path_to_file}
        response = requests.post(self.url + 'upload', headers=headers, params=params )
        response.raise_for_status()
        if response.status_code in range(200, 300):
            print('Success')

    def upload_files_from_a_list(self, unloader):
        print('\n'f'Создание папки BACKUP_UserVK_{unloader.users_id} на Яндекс.Диск')
        directory = 'BACKUP_UserVK_' + unloader.users_id
        self._add_folder(directory)
        for file_name, from_ in unloader._name_creating().items():
            self._upload((directory + '/' + file_name), from_[-1])
            print(f'Выгрузка файла {file_name} на Яндекс.Диск')
        print('\n'
              'Выгрузка файлов на Яндекс.Диск завершена')
        return


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('settings.ini')
    tokenVK = config['VK']['token']
    tokenYa = config['Ya']['token']

    ID = str(input('Введите UserID: '))

    album = str(input('Выберите целевой профиль (по умолчанию загрузится "profile"):\n wall — фотографии со стены\n profile — фотографии профиля: '))
    if album != 'profile' or 'wall':
        album = 'profile'

    unloader = USER_VK(ID, album)

    print(f'Найдено {unloader._get_photo_to_unload_vk()["response"]["count"]} фотографий.')
    count = input('Какое количество фотографий загрузить? (по умолчанию загрузится до 5 фото): ')
    if count == '':
        count = 5

    unloader = USER_VK(ID, album, count)


    uploader = YaUploader(tokenYa)

    uploader.upload_files_from_a_list(unloader)
