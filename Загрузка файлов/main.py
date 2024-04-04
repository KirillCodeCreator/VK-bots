import os

import requests

from auth import get_user_vkapi, GROUP_ID, ALBUM_ID


def main():
    vk_user = get_user_vkapi()
    server_address = vk_user.photos.get_upload_server(group_id=GROUP_ID, album_id=ALBUM_ID)["upload_url"]
    print(server_address)
    os.chdir("static/img")
    files = {}
    for n, photo in enumerate(os.listdir()[:3]):
        path = os.path.abspath(photo)
        files[f"file{n + 1}"] = open(path, "rb")
    resp = requests.post(server_address, files=files)
    json_resp = resp.json()
    vk_user.photos.save(album_id=ALBUM_ID, group_id=GROUP_ID, **json_resp)
    print("=======================")


if __name__ == "__main__":
    main()
