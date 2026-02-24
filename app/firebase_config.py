import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import base64

def get_db():
    if not firebase_admin._apps:
        secret_b64 = os.environ.get("FIREBASE_KEY_BASE64")
        if not secret_b64:
            raise Exception("FIREBASE_KEY_BASE64 not set")

        # Decode once
        secret_json = base64.b64decode(secret_b64).decode("utf-8")
        cred_dict = json.loads(secret_json)

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    return firestore.client()
