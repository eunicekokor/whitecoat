from whitecoat import app
from flask import render_template, request
from datetime import timedelta, datetime

@app.route("/", methods=["GET","POST"])
def index():
	data = {
		"current_time":datetime.now()
	}
	return render_template("index.html", data=data)
