from flask import Flask
from flask import jsonify, request, Response
import auth, utils, json, os.path
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources=r'/api/*', supports_credentials=True)


@app.route("/", methods = ['GET'])
def index():
	token=request.headers.get('token')
	if token:
		if(auth.check_auth(token)):
			return redirect(url_for('dashboard'))
		else:
			content = utils.get_file('index.html')
			return Response(content, mimetype="text/html")
	else:
		content = utils.get_file('index.html')
		return Response(content, mimetype="text/html")

@app.route("/signup", methods = ['GET'])
def signup_page():
	token=request.headers.get('token')
	if token:
		if(auth.check_auth(token)):
			return redirect(url_for('dashboard'))
		else:
			content = utils.get_file('signup.html')
			return Response(content, mimetype="text/html")
	else:
		content = utils.get_file('signup.html')
		return Response(content, mimetype="text/html")


@app.route("/api/login", methods = ['POST'])
@cross_origin(headers=['Content-Type','token'])
def login():
    return auth.login(request.get_json(force=True))


@app.route("/api/signup", methods = ['POST'])
@cross_origin(origin='*', headers=['Content-Type','token'])
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
@cross_origin(headers=['Content-Type','token'])
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


@app.route("/api/message/send", methods = ['POST'])
@cross_origin(headers=['Content-Type','token'])
def send():
	token=request.headers.get('token')
	if token:
		if(auth.check_auth(token)):
			data=request.get_json(force=True)
			return utils.send(data)
		else:
			return jsonify({"msg":"Please login"})
	else:
		return jsonify({"msg":"Please login"})



