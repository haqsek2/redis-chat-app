import re, base64
from config import get_config
from flask import jsonify, request
from datetime import datetime

redis_client = get_config().SESSION_REDIS

def validate_email(email):
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
	if(re.fullmatch(regex, email)):
		return 1
	else:
		return 0

def search(query):
	keys=redis_client.keys('user:*')
	users=[]
	regex = r'\b^user:[\s\d]+$\b'
	my_id=str(request.headers.get('token')).split(':')[-1]
	for key in keys:
		key=key.decode()
		if (re.fullmatch(regex, key) and key.split(":")[-1] != my_id):
			user_id = key
			user=redis_client.hgetall(user_id)
			try:
				if re.search(query,user[b"name"].decode()):
					users.append({"name":user[b"name"].decode(), "id":key.split(":")[-1]})
			except Exception as e:
				pass

	return jsonify({"users":users})

def send(data):
	receiver_id=data["r_id"]
	token=request.headers.get('token')
	sender_id=str(token).split(':')[-1]
	send_time=datetime.now()
	msg=data["msg"]
	next_id = redis_client.incr("total_msgs")
	msg_key = f"msg:{next_id}"
	redis_client.hmset(msg_key, {"sender": sender_id, "receiver": receiver_id, "time":str(send_time), 'msg':str(base64.b64encode(bytes(msg, 'utf-8')))})

	return jsonify({"msg":"message sent","status":"ok"})


