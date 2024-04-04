import json

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

# параметры сообщества
APPTOKEN = "APPTOKEN"
GROUP_ID = 224431580
ALBUM_ID = 302234059

client_id = 6287487
client_secret = "QbYic1K3lEV5kTGiqlq2"
login = 'LOGIN'  # сюда ввести логин аккаунта пользователя
password = 'PASSWORD'  # сюда ввести пароль от аккаунта пользователя


def auth_handler():
    key = input("Введите аутентификационный код: ")
    remember_device = True
    return key, remember_device


# в файл codes.json из проекта надо вставить резервные коды для учетки пользователя
# Надо сходить в Настройки - Безопасность и вход - Двухфакторная аутентификация - Резервные коды
# Вставить коды в файл codes.json, удалив пробелы между цифрами
def auth_handler_with_code():
    with open('../codes.json', mode='r') as file:
        res = json.loads(file.read())
    if len(res) == 0:
        print('Внимание, список кодов пуст, авторизация невозможна')
        return '', False

    key = res[0]
    res.pop(0)
    with open('../codes.json', mode='w') as file:
        json.dump(res, file)
    remember_device = True
    return key, remember_device


def get_user_vkapi():
    vk_user_session = vk_api.VkApi(login, password, app_id=client_id, client_secret=client_secret,
                                   auth_handler=auth_handler_with_code, api_version='5.131')
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_user_session.get_api()


def get_VkBotLongPoll(session):
    return VkBotLongPoll(session, GROUP_ID)


def get_group_session():
    vk_session = vk_api.VkApi(token=APPTOKEN)
    return vk_session


def get_group_vkapi(session):
    return session.get_api()
