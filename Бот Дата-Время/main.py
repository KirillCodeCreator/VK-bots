import datetime
import random

from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi

weekdays = ("Понедельник", "Вторник", "Среда", "Четверг",
            "Пятница", "Суббота", "Воскресенье")


def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_text = event.obj.message["text"]
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            print(f"Получено сообщение от пользователя {user['first_name']}: {msg_text}")
            if any(map(lambda word: word in msg_text.lower(), ("время", "число", "дата", "день"))):
                dt = datetime.datetime.now()
                msg = f"Сегодня {dt.strftime('%d-%m-%Y')}\nВремя {dt.strftime('%H:%M:%S')}\nДень недели {weekdays[dt.weekday()]}"
                vk.messages.send(user_id=usr_id, message=msg,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                msg = f"{user['first_name']}, Вы можете узнать текущие дату и время, для этого в Вашем сообщении должно быть одно из слов: время, дата, число, день"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    main()
