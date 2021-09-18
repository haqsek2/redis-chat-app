from flask import Flask
from flask import jsonify, request
import auth, utils, json

app = Flask(__name__)

@app.route("/api/login", methods = ['POST'])
def login():
    return auth.login(request.get_json(force=True))


@app.route("/api/signup", methods = ['POST'])
def signup():
	data = request.get_json(force=True)
	data=json.dumps(data)
	data = json.loads(str(data))
	email=data["email"]
	password=data["password"]
	name=data["name"]
	# check if values are assigned
	if(email != "" and password != "" and name != ""):
		# validate email
		if(utils.validate_email(email) != 0):
			return auth.create_user(email, password, name)
		else:
			return {"status":"error","msg":"Email is invalid"}
	else:
		return {"status":"error","msg":"All fields are required"}


@app.route("/api/search", methods = ['POST'])
def search():
	token=request.headers.get('token')
	if token:
		if(auth.check_auth(token)):
			data=request.get_json(force=True)
			query=data["query"]
			return utils.search(query)
		else:
			return jsonify({"msg":"Please login"})
	else:
		return jsonify({"msg":"Please login"})
