import datetime
import random
import re

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
            # регулярное выражения для определения наличия даты в формате YYYY-MM-DD
            if re.match("^(([0-9]{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]))$", msg_text):
                year, month, day = map(int, msg_text.split("-"))
                dt = datetime.date(year, month, day)
                msg = f"День недели в тот день: {weekdays[dt.weekday()]}"
                vk.messages.send(user_id=usr_id, message=msg,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                msg = f"{user['first_name']}, введите дату в формате 'ГГГГ-ММ-ДД' ('YYYY-MM-DD') и узнаете день недели"
                vk.messages.send(user_id=usr_id, message=msg,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    main()
