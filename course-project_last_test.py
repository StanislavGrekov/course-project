import requests
import time
import json
from tqdm import tqdm
from time import sleep

class VkUsers:
    url = 'https://api.vk.com/method/'
    def __init__(self, tokenVk):
        self.params = {
            'access_token': tokenVk,
            'v': '5.131'
        }

    def photos(self, id, count_photo):
        '''
        Данный метод выводит в виде словаря ссылки и количество лайков по фотографиям в максимальном
         качестве. Выполняет методы, которые создают папку на я.диске, загружают в нее фото, выдают отчет.
         На вход получает id пользователя VK, количество фото.
        '''
        photos_url = self.url + 'photos.get'
        serch_FAM_params = {
            'owner_id': id,
            'album_id': 'profile',
            'count': count_photo,
            'extended': '1',
            'photo_sizes': '1'

        }
        ya.category_created(category_on_YaDisk) # Запускаем метод, который создаст папку на яндекс диске
        res = requests.get(photos_url, params={**self.params, **serch_FAM_params}).json()
        res = res['response']['items']
        links,likes_all,links_dict = [],[],{}
        for element in res: # Перебираем элементы ответа JSON и заполняем списки
            count = len(element['sizes'])
            count -= 1
            link = element['sizes'][count]['url']
            links.append(link)
            likes = element['likes']['count']
            if likes == 0: # Если кол-во лайков равно 0, то вытаскиваем дату
                likes = time.ctime(int(element['date']))
                Date_Full = likes.split(' ')
                day,month,yaer = Date_Full[3],Date_Full[1],Date_Full[5]
                likes = (day+'.'+month+'.'+yaer)
            likes_all.append(likes)
        links_dict = dict(zip(links,likes_all)) # Делаем словарь, где ключ-ссылка, а значение кол-во лайков(ну или дата)
        for key,values in tqdm(links_dict.items(), desc = 'Files upload'): # Перебираем элементы словаря и запускаем метод загрузки файла на Яндекс диск по ссылке
            category_on_YaDisk_name = category_on_YaDisk+'/'+str(values)+'.jpg'
            URL_file = key
            ya.POST_upload(category_on_YaDisk_name, URL_file)
            sleep(0.1)
        ya.get_info(category_on_YaDisk) # Запускаем метод, который создаст JSON на локальной машине

#############################################################
class YaDisk:
    def __init__(self, tokenYa):
        self.token = tokenYa

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
        Данный метод получает информацию по файлам в каталоге Яндекс.диска, и создает отчет на локальной машине
        (файл - data.json). На вход получает название каталога яндекс диска
        '''
        get_info_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': category_on_YaDisk}
        res = requests.get(get_info_url, params=params, headers=headers).json()
        with open('data.json', 'w') as outfile:
            count = 1
            for element in res['_embedded']['items']:
                json.dump(f'{count})File_name: {element["name"]}, size:{element["size"]}', outfile)
                outfile.write('\n') #не разобрался как в json сделать перенос строки
                count+=1
        print('The file data.json has been generated!')
        print('Congratulations, everything went well!')

    def category_created(self, path_to_file):
        '''
        Данный метод создает каталог на Яндекс.диске. На вход получает название каталога
        '''
        file_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': path_to_file}
        response = requests.put(file_url, headers=headers, params=params)
        status_code = response.status_code
        if status_code == 201:
            print(f'Сategory {path_to_file} created!')
        elif status_code == 409:
            print(f'Category {path_to_file} was created earlier!')

    def POST_upload(self, category_on_YaDisk_name, URL_file):
        '''
        Данный метод копирует в каталог на яндекс.диске файл по его ссылке. На
        вход получает название каталога в который необходимо поместить файл, ссылку с файлом
        '''
        POST_UPLOAD_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': category_on_YaDisk_name, 'url': URL_file}
        requests.post(POST_UPLOAD_URL, params=params, headers=headers)

if __name__ == '__main__':
    #Берем ключи из файлов
    with open('tokenYa.txt', 'r') as file_object:
        tokenYa = file_object.read().strip()
    with open('tokenVk.txt', 'r') as file_object:
        tokenVk = file_object.read().strip()

    def numb():
        '''
        Данная функция проверяет ввели ли мы число. Нужно для проверки ID VK и кол-ва фотографий
        '''
        while True:
            try:
                global number
                number = int(input("Number: "))
                break
                return number
            except ValueError:
                print("Make sure it is a number.")
###### Начало, ввыод приветсвия########
    print('Welcome to our photo backup service!\nInsert ID Vk users\n')
    numb()
    id = number
    print('Insert count photos, which you want copy:\n')
    numb()
    count_photo = number
    category_on_YaDisk = input('Insert name category on Ya.disk:\n')
    # Объявляем экземпляры классов
    vk = VkUsers(tokenVk)
    ya = YaDisk(tokenYa)
    # Запсукаем метод
    vk.photos(id, count_photo)










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
