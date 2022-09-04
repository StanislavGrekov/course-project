import time
import requests
from pprint import pprint
import sys
import os

class VkUsers:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos(self, id):
        '''
        Данный метод выводит в виде списка ссылки на фотографии в максимальном качестве из профиля
        пользователя в VK. На вход получает id пользователя VK
        '''
        photos_url = self.url + 'photos.get'
        serch_FAM_params = {
            'owner_id': id,
            'album_id': 'profile',
            'count': '5',
            'extended': '1',
            'photo_sizes': '1'

        }
        res = requests.get(photos_url, params={**self.params, **serch_FAM_params}).json()
        res = res['response']['items']
        links = []
        for element in res:
            count = len(element['sizes'])
            count -= 1
            link = (element['sizes'][count]['url'])
            links.append(link)
        print('Список ссылок на фотографии в мак.качестве:')
        pprint(links)


#############################################################
class YaDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        '''
        Даный метод возращается heders, используется в других методах при формировании запроса
        '''
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_info(self, category_on_YaDisk):
        '''
        Данная метод получает информацию по файлам в каталоге Яндекс.диска.
        На вход получает название каталога яндекс диска
        '''
        get_info_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': category_on_YaDisk}
        res = requests.get(get_info_url, params=params, headers=headers).json()
        print('Файлы в каталоге:',category_on_YaDisk)
        for element in res['_embedded']['items']:
            pprint(f'Имя файла: {element["name"]}')

    def category_created(self, path_to_file):
        '''
        Данный метод создает каталог на Яндекс.диске. На вход получает название каталога
        '''
        file_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path_to_file, "overwrite": "true"}
        response = requests.put(file_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            print('Сategory created!')

    def POST_upload(self, category_on_YaDisk_name, URL_file):
        '''
        Данный метод копирует в каталог на яндекс.диске файл по его ссылке. На
         вход получает название каталога в который необходимо поместить файл, ссылку с файлом
        '''
        POST_UPLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': category_on_YaDisk_name, 'url': URL_file}
        response = requests.post(POST_UPLOAD_URL, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 202:
            print('File Upload')
        return response.json()


if __name__ == '__main__':
    vk = VkUsers('                    ', '5.131')
    vk.photos('73084815')

    ya = YaDisk('                    ')
    category_on_YaDisk = 'load' # название каталога на Я.диске
    #ya.category_created(category_on_YaDisk) # вызов метода, который создаст каталог
    category_on_YaDisk_name = 'load/test4.jpg' # название каталога и файла в нем
    URL_file = "https://sun9-37.userapi.com/impf/mGpjjYfl6k__fVVnGJtk2wsUhGnH5rHXkWARJw/7JWT6iRYxvk.jpg?size=700x516&quality=96&sign=308404409a760fc1db73b34e9da43160&c_uniq_tag=in8t7_ETNA2g9o98aV9jjp97ezlopVu27fSbGtMdpT0&type=album"
    ya.POST_upload(category_on_YaDisk_name, URL_file)  # вызов метода, который загружает фото
    ya.get_info(category_on_YaDisk) # получаение информации по каталогу, сначала в папку необходимо загрузить фото

    '''
    Пока реализовал в 'ручном режиме'. Метод vk.photos('73084815') выдает список ссылок, которые мы 
    должны 'руками' копировать в переменную URL_file. Затем мы выполняем методы, которые из ВК по ссылкам копируют
    фотографии на Яндекс диск.
    
    Инструкция:
    1. При первом запуске нужно раскомментировать метод ya.category_created - это нужно для создания каталога
    на Яндекс диске.
    2. Затем, мы его комментируем (ya.category_created) - это нужно чтобы программа не падала с ошибкой 409
    Указанного пути "{path}" не существует.
    
    Вопросы:
    1.Почему при повторном вызове ya.category_created программа падает с ошибкой 409 хотя я в параметрах 
    данного метода указываю "overwrite": "true", по идее папка должна перезаписаться. Или это не так работает?
    2. Как мне релизовать выполнение методов, чтобы при первом запуске категория создавалась (выполнялся метод
    ya.category_created), а затем уже этот метод не вызывался?
    3. У меня сделаны 2 отдельных класса, правильнее будет сделать один родительский, а другой дочерний? 
    Или это не принципиально? 
    4. Метод get_info работает с задержкой. Т.е. если мы выполним методы как они приведены, вернется пустой результат.
    Хотя POST_upload стоит перед get_info и отрабатывает корректно. Не подскажите почему так?
    
    Пока не реализовал:
    1. Вывод необходимой информации (лайки) по файлам в категории,
    2. Прогресс-бар или логирование для отслеживания процесса программы,
    3. Зависимости requiremеnts.txt.
    
    '''
