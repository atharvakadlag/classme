from app import app
from flask import redirect
from datetime import datetime, timedelta
import json
from pytz import timezone
from os import environ
INTZ = timezone('Asia/Kolkata')

def inc_count():
    count = int(environ["COUNT"])
    count += 1
    print(f"Website accessed {count} times")
    environ["COUNT"] = str(count)

def load_links(file_name = "classlinks.json"):
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data

def get_current_class():
    detla = timedelta(minutes=30)
    now = datetime.now(INTZ) + detla

    day = datetime.today().strftime("%A").lower()
    data = load_links()[day]

    hours = now.strftime("%H")
    minutes = now.strftime("%M")

    now_str = str(hours).zfill(2) + ":" + str(minutes).zfill(2)
    now = datetime.strptime(now_str, "%H:%M")
    print(now)
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
    inc_count()
    return "<center><img src='/static/timetable.png' width='100%'></center><br><center><a href='/coe'>COE</a> <a href='/ced'>CED</a></center>"

@app.route('/coe')
def coe():
    inc_count()
    current_class = get_current_class()
    if current_class is None:
        return redirect('/noclass')
    return redirect(current_class["link"]["coe"], code=302)

@app.route('/ced')
def ced():
    inc_count()
    current_class = get_current_class()
    if current_class is None:
        return redirect('/noclass')
    return redirect(current_class["link"]["ced"], code=302)

@app.route('/noclass')
def noclass():
    return "<center>No class right now!!</center>"
