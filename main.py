import datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

token = "vk1.a.2l-SDnF6CViDvFDPKWE_tqkmNFMEBJ42vdAogawnAvksla0YfM7FSQ-YPONjsPVY0PJlgVe1NZU_i4J2u0ffc_iQbMJob0Zj491r8EgRqz4kUtAZNo3P4n62nCrGRcfsiWp-9N4CHpnyxsyza2fbLUFHwFyjPu2KlCtB-gnakSU8fM95DQqlNqaRVhrx7YrVVEYG1GkOuaiBgzohHsmnNw"
idpub = 224431580
weekdays = ("Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье")


def main():
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, idpub)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
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
            if any(map(lambda word: word in msg_text.lower(), ("время", "число", "дата", "день"))):
                dt = datetime.datetime.now()
                msg = f"Сегодня {dt.strftime('%d-%m-%Y')}\nВремя {dt.strftime('%H:%M:%S')}\nДень недели {weekdays[dt.weekday()]}"
                vk.messages.send(user_id=usr_id, message=msg,
                             random_id=random.randint(0, 2 ** 64))
            else:
                msg =f"{user['first_name']}, Вы можете узнать текущие дату и время, для этого в Вашем сообщении должно быть одно из слов: время, дата, число, день"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))





if __name__ == "__main__":
    main()
