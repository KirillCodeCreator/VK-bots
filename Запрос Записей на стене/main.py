import datetime

from auth import get_user_vkapi


def main():
    vk_user = get_user_vkapi()
    resp = vk_user.wall.get(count=5, offset=0)
    if resp["items"]:
        for item in resp["items"]:
            text = item["text"]
            date = item["date"]
            dt = datetime.datetime.fromtimestamp(int(date))
            print(text + ";")
            print(f"date: {dt.date()}, time: {dt.time()}")


if __name__ == "__main__":
    main()
