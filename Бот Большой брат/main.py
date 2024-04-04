import random

from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi


def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            name = vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']
            try:
                city = vk.users.get(user_id=event.obj.message['from_id'], fields=['city'])[0]['city']['title']
            except Exception:
                city = ''
            if not city:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {name}",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {name}\nКак поживает {city}?",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    main()
