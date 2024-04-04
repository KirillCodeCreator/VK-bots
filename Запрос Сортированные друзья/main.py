from auth import get_user_vkapi


def main():
    vk_user = get_user_vkapi()
    resp = vk_user.friends.get(fields="bdate")
    if resp["items"]:
        for item in sorted(resp["items"], key=lambda val: (val["last_name"], val["first_name"])):
            if item.get("first_name", "") != "DELETED":
                print(item.get("last_name", ""), item.get(
                    "first_name", ""), item.get("bdate", ""))


if __name__ == "__main__":
    main()
