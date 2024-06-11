# Define a custom function to serialize datetime objects 
import datetime 
import json 
import random
import string
import base64
import jwt
import os



def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    return str(obj)
    #raise TypeError("Type not serializable") 

def myjson(rows):

    if isinstance(rows, list):
        data = []
        for row in rows:
            data.append(row.toDict()) 

        json_data = json.dumps(data, default=serialize_datetime) 
        return json_data
    else:
        json_data = json.dumps(rows, default=serialize_datetime) 
        return json_data

def randomstr(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def extract_bearer_token(header):
    if header:
        token_parts = header.split(' ')
        if len(token_parts) == 2 and token_parts[0].lower() == 'bearer':
            token = token_parts[1]
            # Now you have the bearer token in the 'token' variable
            # Validate the token, check permissions, etc.
            try:
                decoded_token = decode_base64(token)
                decoded_payload = jwt.decode(decoded_token, os.environ.get("jwtkey"), algorithms=["HS256"])
                return decoded_payload
            except:
                return None
        else:
            return None
    else:
        return None
    
def encode_to_base64(text):
    """Encodes a string to Base64 and returns the encoded string."""
    message_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    return base64_message

def decode_base64(encoded_string):
    """Decodes a Base64 string and returns the original string."""
    # Decode Base64 bytes
    base64_bytes = encoded_string.encode('utf-8')  # Convert to bytes (required for decoding)
    message_bytes = base64.b64decode(base64_bytes)
    # Convert bytes back to string
    decoded_string = message_bytes.decode('utf-8')
    return decoded_string

def get_encoded_payload(payload):
    print(payload)
    encoded_jwt = jwt.encode(payload, os.environ.get("jwtkey"), algorithm="HS256")
    print (encoded_jwt)
    encoded_token = encode_to_base64(encoded_jwt)
    return encoded_token
    

