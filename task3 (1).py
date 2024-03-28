import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():

    longpoll = VkBotLongPoll(vk_session, 225297829)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message="Спасибо, что написали нам. Мы обязательно ответим",
                             random_id=random.randint(0, 2 ** 64))

    if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
        print(f'Печатает {event.obj.from_id} для {event.obj.to_id}')

    if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
        print(f'Печатает {event.obj.from_id} для {event.obj.to_id}')


if __name__ == '__main__':
    main()
