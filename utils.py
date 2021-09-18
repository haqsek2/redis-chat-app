import re
from config import get_config
from flask import jsonify, request

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
