import random

import requests
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi

MAP_API_SERVER = 'https://static-maps.yandex.ru/1.x/'
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"

MAP_TMP_FILENAME = 'map.png'
MAP_LAYERS = ('map', 'sat', 'sat,skl')

GEOCODER_APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_map_attachment(lon, lat, map_type, vk_upload, peer_id):
    url = f"https://static-maps.yandex.ru/1.x/?ll={lat},{lon}&z=12&l={map_type}"
    response = requests.get(url)
    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        return None

    with open(MAP_TMP_FILENAME, 'wb') as img_file:
        img_file.write(response.content)
        photo = vk_upload.photo_messages(photos=MAP_TMP_FILENAME)
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        return attachment


def get_coordinates(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": GEOCODER_APIKEY,
            'geocode': city_name,
            'format': 'json'
        }
        response = requests.get(url, params)
        if not response:
            print('Произошла ошибка при получении координат.')
            print(f'{response.status_code}: {response.reason}')
            print(response.text)
            return None

        json = response.json()
        coordinates_str = json['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        long, lat = map(float, coordinates_str.split())
        return long, lat
    except Exception as e:
        print(e)
        return None, None


def get_map_type(message):
    map_type = MAP_LAYERS[1]
    if message == "Схема":
        map_type = MAP_LAYERS[0]
    elif message == "Гибрид":
        map_type = MAP_LAYERS[2]
    return map_type


def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    vk_upload = VkUpload(vk)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    need_city = True
    city = None
    first = True
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.obj.message['text'])
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            if first:
                first = False
                msg = f"{user['first_name']}, введи название местности, которую хочешь увидеть"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))
                continue
            elif need_city:
                city = event.obj.message['text']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Отлично, выбери тип карты",
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('keyboard_show.json', "r", encoding="UTF-8").read())
                need_city = not need_city
            else:
                map_type = get_map_type(event.obj.message['text'])
                long, lat = get_coordinates(city)
                if long is None:
                    msg = f"{user['first_name']}, не нашли такого места. Введи название местности, которую хочешь увидеть"
                    vk.messages.send(user_id=usr_id,
                                     message=msg,
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    pic = get_map_attachment(lat, long, map_type, vk_upload, event.obj.message['peer_id'])
                    vk.messages.send(random_id=random.randint(0, 2 ** 64),
                                     attachment=pic,
                                     user_id=event.obj.message['from_id'],
                                     message=f"Это {city}. Что вы еще хотите увидеть?")
                need_city = not need_city


if __name__ == "__main__":
    main()
