import random

import requests
import wikipedia
from vk_api.bot_longpoll import VkBotEventType

from auth import get_group_session, get_group_vkapi, get_VkBotLongPoll

wikipedia.set_lang('ru')


def main():
    vk_session = get_group_session()
    vk = get_group_vkapi(vk_session)
    longpoll = get_VkBotLongPoll(vk_session)
    print("Ожидаем сообщения от пользователя...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                usr_id = event.obj.message["from_id"]
                user = vk.users.get(user_ids=str(usr_id))[0]
                msg = f"{user['first_name']}, запрос получен, мы пошли искать на википедии..."
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))
                print(f"От пользователя {user['first_name']} запрос получен, пошли искать на википедии...")
                wikiresponse = wikipedia.summary(f"{event.obj.message['text']}", sentences=5)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{wikiresponse}",
                                 random_id=random.randint(0, 2 ** 64))
                print(f"Пользователю {user['first_name']} отправлен ответ")
                msg = f"{user['first_name']}, можешь спрашивать снова"
                vk.messages.send(user_id=usr_id, message=msg, random_id=random.randint(0, 2 ** 64))
            except wikipedia.exceptions.DisambiguationError:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{user['first_name']}, Вики сообщило, что много материала может относиться к твоему сообщению. Напиши точнее.",
                                 random_id=random.randint(0, 2 ** 64))
                print("Сообщение не точное")
            except wikipedia.exceptions.PageError:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{user['first_name']}, увы, на Википедии ничего не найдено. Может попробуешь еще раз?",
                                 random_id=random.randint(0, 2 ** 64))
                print("Ничего не найдено")
            except requests.exceptions.ConnectTimeout:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{user['first_name']}, увы, Википедия долго не отвечала, наверное ничего не найдено. Может попробуешь еще раз?",
                                 random_id=random.randint(0, 2 ** 64))
                print("Википедия долго не отвечала")
            except Exception as err:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{user['first_name']}, увы, ошибка, наверное ничего не найдено. Может попробуешь еще раз?",
                                 random_id=random.randint(0, 2 ** 64))
                print(err.__str__())


if __name__ == "__main__":
    main()
