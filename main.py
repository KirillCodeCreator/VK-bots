import datetime
import re

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

token = "vk1.a.2l-SDnF6CViDvFDPKWE_tqkmNFMEBJ42vdAogawnAvksla0YfM7FSQ-YPONjsPVY0PJlgVe1NZU_i4J2u0ffc_iQbMJob0Zj491r8EgRqz4kUtAZNo3P4n62nCrGRcfsiWp-9N4CHpnyxsyza2fbLUFHwFyjPu2KlCtB-gnakSU8fM95DQqlNqaRVhrx7YrVVEYG1GkOuaiBgzohHsmnNw"
idpub = 224431580
weekdays = ("Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье")
album_id = 302234059

def auth_handler():
    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device

def main():
    login, password = 'login', 'password'
    vk_user_session = vk_api.VkApi(login, password, app_id=6287487, client_secret="QbYic1K3lEV5kTGiqlq2", auth_handler=auth_handler)
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk_user = vk_user_session.get_api()

    vk_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, idpub)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        # решение для задачи Бот Большой брат
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_text = event.obj.message["text"]
            usr_id = event.obj.message["from_id"]
            vk = vk_session.get_api()
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            print (f"Получено сообщение от пользователя {user['first_name']}: {msg_text}")
            msg = f"Привет, {user['first_name']}!"
            if user["city"]:
                msg += f"\nКак поживает {user['city']['title']}?"
            vk.messages.send(user_id=usr_id, message=msg,
                             random_id=random.randint(0, 2 ** 64))

            # решение для задачи Бот Дата-Время
            if any(map(lambda word: word in msg_text.lower(), ("время", "число", "дата", "день"))):
                dt = datetime.datetime.now()
                msg = f"Сегодня {dt.strftime('%d-%m-%Y')}\nВремя {dt.strftime('%H:%M:%S')}\nДень недели {weekdays[dt.weekday()]}"
                vk.messages.send(user_id=usr_id, message=msg,
                             random_id=random.randint(0, 2 ** 64))
            else:
                msg =f"{user['first_name']}, Вы можете узнать текущие дату и время, для этого в Вашем сообщении должно быть одно из слов: время, дата, число, день"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))

            #решение для задачи Бот дня недели
            if re.match("^(([0-9]{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]))$", msg_text):
                year, month, day = map(int, msg_text.split("-"))
                dt = datetime.date(year, month, day)
                msg = f"День недели в тот день: {weekdays[dt.weekday()]}"
                vk.messages.send(user_id=usr_id, message=msg,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                msg = "Введите дату в формате 'ГГГГ-ММ-ДД' ('YYYY-MM-DD')"
                vk.messages.send(user_id=usr_id, message=msg,
                                 random_id=random.randint(0, 2 ** 64))

            #решение для задачи Получение фотографий из альбома
            if any(map(lambda word: word in msg_text.lower(), ("фото", "альбом"))):
                resp = vk_user.photos.get(group_id=idpub, album_id=album_id, count=100, offset=0)
                if resp["items"]:
                    for item in resp["items"]:
                        photos = sorted(item["sizes"], key=lambda val: (-val["height"]))
                        width = photos[0].get("width", "")
                        height = photos[0].get("height", "")
                        url = photos[0].get("url", "")
                        vk.messages.send(user_id=usr_id, message=f'Размеры {width}х{height}\nurl = {url}', random_id=random.randint(0, 2 ** 64))
            else:
                msg = f"{user['first_name']}, Вы можете получить фото из альбома, для этого в Вашем сообщении должно быть одно из слов: фото, альбом"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))

if __name__ == "__main__":
    main()
