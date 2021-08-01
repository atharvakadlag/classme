from app import app
from flask import redirect
from datetime import datetime, timedelta
import json

def load_links(file_name = "classlinks.json"):
    # load the given json file
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data

def get_current_class():
    detla = timedelta(minutes=10)
    now = datetime.now() - detla

    day = datetime.today().strftime("%A").lower()
    data = load_links()[day]

    hours = now.strftime("%H")
    minutes = now.strftime("%M")

    now_str = str(hours).zfill(2) + ":" + str(minutes).zfill(2)
    now = datetime.strptime(now_str, "%H:%M")

    for key in data.keys():
        times = key.split("-")
        start_time = times[0]
        start_time = datetime.strptime(times[0], "%H:%M")
        end_time = datetime.strptime(times[1], "%H:%M")
        
        if now >= start_time and now <= end_time:
            return data[key]


@app.route('/')
@app.route('/index')
def index():
    current_class = get_current_class()
    if current_class is None:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ?ak-says=no-class-right-now", code=302)
    return redirect(current_class["link"], code=302)