import vk_api
# group_id = 224431580
from flask import Flask, render_template

from auth import get_user_vkapi, get_group_vkapi, get_group_session

app = Flask(__name__)


@app.route('/vk_stat/<int:group_id>')
def vk_stat(group_id):
    vk = get_user_vkapi()
    try:
        response = vk.stats.get(group_id=group_id, fields="reach")
    except vk_api.exceptions.ApiError:
        return "Произошла ошибка..."
    activities = {
        'likes': 0,
        'comments': 0,
        'subscribed': 0
    }
    ages = {
        "12-18": 0,
        "18-21": 0,
        "21-24": 0,
        "24-27": 0,
        "27-30": 0,
        "30-35": 0,
        "35-45": 0,
        "45-100": 0
    }
    cities = set()
    if response:
        for item in response[:10]:
            try:
                if item.get("activity") != None:
                    activities['likes'] += item['activity'].get('likes', 0)
                    activities['comments'] += item['activity'].get('comments', 0)
                    activities['subscribed'] += item['activity'].get('subscribed', 0)
                for age in item['reach']['age']:
                    ages[age['value']] += age['count']
                for city in item['reach']['cities']:
                    cities.add(city['name'])
            except Exception:
                continue

    return render_template('vk.html', activities=activities.items(), age=ages.items(), cities=cities)


if __name__ == '__main__':
    app.run()
