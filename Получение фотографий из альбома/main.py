import random

from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_VkBotLongPoll, get_group_vkapi, get_user_vkapi, GROUP_ID, ALBUM_ID

def main():
    vk_session = get_group_session()
    vk_user = get_user_vkapi()
    vk = get_group_vkapi(vk_session)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg_text = event.obj.message["text"]
            usr_id = event.obj.message["from_id"]
            user = vk.users.get(user_ids=str(usr_id), fields="city")[0]
            print(f"Получено сообщение от пользователя {user['first_name']}: {msg_text}")
            if any(map(lambda word: word in msg_text.lower(), ("фото", "альбом"))):
                resp = vk_user.photos.get(group_id=GROUP_ID, album_id=ALBUM_ID, count=100, offset=0)
                if resp["items"]:
                    for item in resp["items"]:
                        photos = sorted(item["sizes"], key=lambda val: (-val["height"]))
                        width = photos[0].get("width", "")
                        height = photos[0].get("height", "")
                        url = photos[0].get("url", "")
                        vk.messages.send(user_id=usr_id, message=f'Размеры {width}х{height}\nurl = {url}',
                                         random_id=random.randint(0, 2 ** 64))
            else:
                msg = f"{user['first_name']}, Вы можете получить фото из альбома, для этого в Вашем сообщении должно быть одно из слов: фото, альбом"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))


if __name__ == "__main__":
    main()
