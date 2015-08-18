from whitecoat import app
from flask import render_template, request, redirect, g
from datetime import timedelta, datetime
from twilio.rest import TwilioRestClient
from psycopg2 import connect, extras
from config import *
import json
import sqlite3

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
DATABASE_URL = DATABASE_URL

#
# Setup for DB
#
def dict_cursor(conn, cursor_factory=extras.RealDictCursor):
    return conn.cursor(cursor_factory=cursor_factory)

@app.route("/", methods=["GET","POST"])
def index():
  data = {}
  messages = client.messages.list()
  data["messages"] = []
  print len(messages)
  for message in messages[33:]:
    print "\n" + str(message.body)
    if not message.body.lower().startswith("from:") and "test" not in message.body.lower():
      #print "\n" + str(message.body)
      data["messages"].append(message.body)
  
  if request.method=="POST":
    text = request.form.get("text", "A message")
    name = request.form.get("name", "Eunice")
    body = text + "\nFrom: " + name
    data["message"] = body
    client.messages.create(
                           to="+17149075336",
                           from_="+15627310871",
                           body=body)

  return render_template("index.html", data=data)

feelings = {
    "happy": {
      "message":"That's great! On a scale of 1 to 5, How happy are you?",
      "emoji": "128516",
      "options": ["1 - A Little Happy", "2 - Kinda Happy", "3 - Pretty Happy", "4 - Delightfully Happy", "5 - Ecstatic!!!"]
    },
    "sad": {
      "message":"Sorry that you are sad. Why are you feeling sad?",
      "emoji": "128557",
      "options": ["Did your pet die?", "Did your family member die?", 
      "Did your prom date stand you up?", "Did you get hurt?", 
      "Did an important item of yours break?", "Other"]
    },
    "disgust": {
      "message":"Sorry you are disgusted. What is making you disgusted?",
      "emoji": "128541",
      "options": ["Is someone being mean to you?", "Is the temperature too hot?", 
      "Is the food you're eating gross?", "Are you too sweaty?",
      "Are there burping/farting people around you?", "Other"]
    },
    "angry": {
      "message": "Sorry you are angry. What is making you angry?",
      "emoji":"128545",
      "options": ["Did you get into a fight?", "Is someone being mean to you?",
      "Are you trying to fix sommething that isn't working?", "Are your kids annoying you?",
      "Are people playing unfairly?", "Other"]
    }
  }

@app.route("/feelings", methods=["GET","POST"])
def feelings_fxn():
  final_dict = {}
  if request.method == "POST":
    key = request.form.get('yolo', "feeling")
    if key.startswith("happy"):
      value = request.form['yolo'].split("_")
      key = value[0]
      value = int(value[1])
    else:
      value = len(request.form.getlist('yolo'))
    
    final_dict = {
      "final_key": "",
      "final_message": "",
      "recommendation": {
        "sad":["https://www.youtube.com/embed/Q-GLuydiMe4","https://www.youtube.com/embed/__VqT6jhblQ"],
        "happy":["https://www.youtube.com/embed/IKjJ6DQF7xY?start=15&amp;","https://www.youtube.com/embed/Oce4ber3Hko"],
        "angry":["https://www.youtube.com/embed/WHRnvjCkTsw","https://www.youtube.com/embed/sbNZ1pi2Us8"],
        "disgust":["https://www.youtube.com/embed/xEycwV-JUtc", "https://www.youtube.com/embed/5YL3LT1ZvOM?start=16&amp;"]
      },
      "value": 0
    }

    final_dict['final_key'] = key


    if value == 0:
      final_dict['value'] = 0
      final_dict['final_message'] = "You are not even " + str(key) + " anything at all! Did you click on the wrong emotion?"
    elif value == 1 or value == 2:
      final_dict['value'] = 1
      if key == "disgust":
        final_dict['final_message'] = "You are kind of " + key + "ed. It's okay. Try to keep a good level of being " + key + "ed. Wait a little, it will all be okay."
      else:
        final_dict['final_message'] = "You are kind of " + key + ". It's okay. Try to keep a good level of being " + key + ". Wait a little, it will all be okay."
    else:
      final_dict['value'] = 3
      final_dict['final_message'] = "You are very " + key + ". We picked a video just for you to help with that feeling."

    with connect(DATABASE_URL) as conn:
      with dict_cursor(conn) as db:
        '''Setup light database '''

        q = ''' INSERT INTO all_feelings (time, feeling, intensity) 
        VALUES ( %(time)s, %(feeling)s, %(intensity)s) '''
        # Insert a row of data
        db.execute(q, {"time":datetime.now(), "feeling":final_dict['final_key'], "intensity":final_dict['value']})

  
  return render_template("feelings.html", feelings=feelings, final_dict=final_dict)

@app.route("/feelings/feelings-graph", methods=["GET","POST"])
def graph():
  data = {}
  def get_happy_count(db):
    q = '''SELECT COUNT(*) FROM all_feelings WHERE feeling=\'happy\' '''
    db.execute(q)
    count = db.fetchone()
    count['happy'] = count.pop('count')
    count['happy'] = int(count['happy'])
    return count

  def get_sad_count(db):
    q = '''SELECT COUNT(*) FROM all_feelings WHERE feeling=\'sad\' '''
    db.execute(q)
    count = db.fetchone()
    count['sad'] = count.pop('count')
    count['sad'] = int(count['sad'])
    return count

  def get_angry_count(db):
    q = '''SELECT COUNT(*) FROM all_feelings WHERE feeling=\'angry\' '''
    db.execute(q)
    count = db.fetchone()
    count['angry'] = count.pop('count')
    count['angry'] = int(count['angry'])
    return count

  def get_disgust_count(db):
    q = '''SELECT COUNT(*) FROM all_feelings WHERE feeling=\'disgust\' '''
    db.execute(q)
    count = db.fetchone()
    count['disgust'] = count.pop('count')
    count['disgust'] = int(count['disgust'])
    return count

  def get_all_feelings(db):
    q = '''SELECT * FROM all_feelings'''
    db.execute(q)
    data = db.fetchall()
    
    for entry in data:
      entry['time'] = entry['time'].strftime('%A %d %b %Y %l:%M %p')
    return data

  with connect(DATABASE_URL) as conn:
      with dict_cursor(conn) as db:
        data = get_all_feelings(db)

        counts = []
        counts.append(get_happy_count(db))
        counts.append(get_sad_count(db))
        counts.append(get_disgust_count(db))
        counts.append(get_angry_count(db))

  return render_template("graph.html", data=data, counts=counts)