from flask import Flask
from flask import jsonify, request
import auth, utils

app = Flask(__name__)

@app.route("/login")
def login():
    return "wokring"


@app.route("/signup")
def signup():
	email = request.args.get('email') if 'email' in request.args else ""
	password = request.args.get('password') if 'password' in request.args else ""
	name = request.args.get('name') if 'name' in request.args else ""

	# check if values are assigned
	if(email != "" and password != "" and name != ""):
		# validate email
		if(utils.validate_email(email) != 0):
			return auth.create_user(email, password, name)
		else:
			return {"status":"error","msg":"Email is invalid"}
	else:
		return {"status":"error","msg":"All fields are required"}