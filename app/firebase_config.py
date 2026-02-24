import os
import firebase_admin
from firebase_admin import credentials, firestore
import base64

def get_db():
    if not firebase_admin._apps:
        key_path = "app/firebase_key.json"

        # Create key file from secret if it doesn't exist
        if not os.path.exists(key_path):
            secret_b64 = os.environ.get("FIREBASE_KEY_BASE64")
            if not secret_b64:
                raise Exception("FIREBASE_KEY_BASE64 not set")
            with open(key_path, "wb") as f:
                f.write(base64.b64decode(secret_b64))

        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()
