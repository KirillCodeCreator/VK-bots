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
            msg_text = event.obj.message["text"]
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            print(f"Получено сообщение от пользователя {user['first_name']}: {msg_text}")
            msg = f"Привет, {user['first_name']}!"
            if user["city"]:
                msg += f"\nКак поживает {user['city']['title']}?"
            vk.messages.send(user_id=usr_id, message=msg,
                             random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    main()
