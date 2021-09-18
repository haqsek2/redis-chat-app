from config import get_config
import json, math, random, bcrypt

redis_client = get_config().redis_client

def make_email_key(email):
    return f"email:{email}"

def make_name_key(name):
    return f"name:{name}"

def create_user(email, password, name):
    #print(redis_client.keys(pattern='email:'+str(email)))

    #check if email already exists
    if ( redis_client.keys(pattern='email:'+str(email)) != [] ):
        print(redis_client.keys("email:{email}"))
        return {"status":"error","msg": "email already exists"}
    
    # Create a user
    else:
        email_key = make_email_key(email)
        
        hashed_password = bcrypt.hashpw(str(password).encode("utf-8"), bcrypt.gensalt(20))
        next_id = redis_client.incr("total_users")
        user_key = f"user:{next_id}"
        redis_client.set(email_key, user_key)
        redis_client.hmset(user_key, {"email": email, "password": hashed_password})

        redis_client.sadd(f"user:{next_id}:rooms", "0")

        return {"status":"ok","id": next_id, "email": email}