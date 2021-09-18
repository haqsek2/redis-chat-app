from config import get_config
import json, math, random, bcrypt, utils
from flask import jsonify
import hashlib

redis_client = get_config().SESSION_REDIS

def make_email_key(email):
    return f"email:{email}"

def make_name_key(name):
    return f"name:{name}"

def make_pass_key(password):
    return f"password:{password}"

def create_user(email, password, name):
    #print(redis_client.keys(pattern='email:'+str(email)))

    #check if email already exists
    if ( redis_client.keys(pattern='email:'+str(email)) != [] ):
        return {"status":"error","msg": "email already exists"}
    
    # Create a user
    else:
        email_key = make_email_key(email)
        m = hashlib.sha512()
        m.update(str(password).encode("utf-8"))
        hashed_password = m.hexdigest()
        next_id = redis_client.incr("total_users")
        user_key = f"user:{next_id}"
        redis_client.set(email_key, user_key)
        redis_client.set(make_name_key(name), user_key)
        redis_client.set(make_pass_key(hashed_password), user_key)
        redis_client.hmset(user_key, {"email": email, "password": hashed_password, "name":name})

        redis_client.sadd(f"user:{next_id}:rooms", "0")

        return {"status":"ok","id": next_id, "email": email}


def login(data):
    username = data["email"]
    password = data["password"]
    
    username_key = make_email_key(username)
    user_exists = redis_client.exists(username_key)
    
    if user_exists:
        
        user_key = redis_client.get(username_key).decode("utf-8")
        data = redis_client.hgetall(user_key)
        m = hashlib.sha512()
        m.update(str(password).encode("utf-8"))
        hashed_password = m.hexdigest()

        if (hashed_password == data[b"password"].decode()):
            user = {"id": user_key.split(":")[-1], "email": username,"name":data[b"name"]}
            #session["user"] = user
            return user

    return jsonify({"msg": "Invalid username or password"})