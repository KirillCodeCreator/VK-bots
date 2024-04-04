import random

import requests
from vk_api.bot_longpoll import VkBotEventType
from vk_api import VkUpload

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi

MAP_API_SERVER = 'https://static-maps.yandex.ru/1.x/'
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"

MAP_TMP_FILENAME = 'map.png'
MAP_IMG_SIZE = '600,450'
MAP_LAYERS = ('map', 'sat', 'sat,skl')

GEOCODER_APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"
SEARCH_MAPS_APIKEY = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

def get_toponym(address):
    params = {
        "apikey": GEOCODER_APIKEY,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(GEOCODER_API_SERVER, params=params)

    if not response:
        print("Ошибка получения топонима:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")

    json_response = response.json()
    return json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

def show_map(lon, lat, map_type, vk_upload, peer_id):
    params = {
        'z': 23,
        'll': f'{round(lon, 6)},{round(lat, 6)}',
        'l': map_type,
        'size': MAP_IMG_SIZE
    }

    response = requests.get(MAP_API_SERVER, params=params)

    if not response:
        print('Произошла ошибка при получении карты.')
        print(f'{response.status_code}: {response.reason}')
        print(response.text)
        return None

    with open(MAP_TMP_FILENAME, 'wb') as img_file:
        img_file.write(response.content)
        upload_image = vk_upload.photo_messages(photos=img_file, peer_id=peer_id)[0]
        pic = 'photo{}_{}'.format(upload_image['owner_id'], upload_image['id'])
        return pic

def get_toponym_lonlat(toponym):
    toponym_pos = toponym["Point"]["pos"]
    lo, la = map(float, toponym_pos.split(" "))
    return (lo, la)

def get_coordinates(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": GEOCODER_APIKEY,
            'geocode': city_name,
            'format': 'json'
        }
        response = requests.get(url, params)
        json = response.json()
        # получаем координаты города
        # (там написаны долгота(longitude), широта(latitude) через пробел)
        coordinates_str = json['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        long, lat = map(float, coordinates_str.split())
        return long, lat
    except Exception as e:
        return e

def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    vk_upload = VkUpload(vk)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    need_city = True
    city = None
    first = False
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            if not first:
                first = True
                msg = f"{user['first_name']}, введи название местности, которую хочешь увидеть"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))
                continue
            if need_city:
                city = event.obj.message['text']
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Отлично, выбери тип карты",
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('keyboard.json', "r", encoding="UTF-8").read())
                need_city = not need_city
            else:
                long, lat = get_coordinates(city)
                pic = show_map(lat, long, 'map', vk_upload, event.obj.message['peer_id'])
                vk.messages.send(chat_id=event['chat_id'], random_id=random.randint(0, 2 ** 64), attachment=pic, message=f"Это {city}. Что вы еще хотите увидеть?")
                '''with open('**название файла**', 'wb') as img_file:
                    upload_image = upload.photo_messages(photos=img_file, peer_id= ** номер
                    чата + 2000000000 **)[0]
                    pic = 'photo{}_{}'.format(upload_image['owner_id'], upload_image['id'])
                vk.messages.send(chat_id='2',random_id = '',attachment = pic,message = '.')'''
                '''img_file = get_map_png(city)
                upload_image = vk_upload.photo_messages(photos=img_file, peer_id=event.obj.message['peer_id'])[0]
                pic = 'photo{}_{}'.format(upload_image['owner_id'], upload_image['id'])'''

                '''vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Это {city}. Что вы еще хотите увидеть?",
                                 random_id=random.randint(0, 2 ** 64),
                                 keyboard=open('keyboard_hide.json', "r", encoding="UTF-8").read(),
                                 attachment=get_map_png(city))'''
                need_city = not need_city


if __name__ == "__main__":
    main()
