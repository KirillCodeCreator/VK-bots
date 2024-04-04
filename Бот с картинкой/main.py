import random

from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi, get_user_vkapi, GROUP_ID, ALBUM_ID

def get_random_photo_id():
    vk_user = get_user_vkapi()
    response = vk_user.photos.get(album_id=ALBUM_ID, group_id=GROUP_ID)['items']
    photo = response[random.randint(0, len(response) - 1)]
    return f"photo{photo['owner_id']}_{photo['id']}"

def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            msg_text = event.obj.message["text"]
            print(f"Получено сообщение от пользователя {user['first_name']}: {msg_text}")
            msg = f"{user['first_name']}, запрос получен, мы пошли искать фото..."
            vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"{user['first_name']}, отправляю случайную фотографию из основного альбома",
                             random_id=random.randint(0, 2 ** 64),
                             attachment=get_random_photo_id())
            print("Фото отправлено")


if __name__ == "__main__":
    main()
