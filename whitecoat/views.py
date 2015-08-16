from whitecoat import app
from flask import render_template, request, redirect
from datetime import timedelta, datetime
from twilio.rest import TwilioRestClient
from config import *

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 

@app.route("/", methods=["GET","POST"])
def index():
  data = {}
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
