from whitecoat import app
from flask import render_template, request, redirect
from datetime import timedelta, datetime
from twilio.rest import TwilioRestClient
from config import *

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 

@app.route("/", methods=["GET","POST"])
def index():
  if request.method=="POST":
    print "\n\n\ngot here"
    text = request.form.get("text", "A message")

    name = request.form.get("name", "Eunice")
    body = text + "\nFrom: " + name
    client.messages.create(
                           to="+17149075336",
                           from_="+15627310871",
                           body=body)
    print "\n\n\ngot here"
    return redirect(url_for('index'), name=name)
  else:
    data = {}
    return render_template("index.html", data=data)
