import os
import firebase_admin
from firebase_admin import credentials, firestore
import json

def get_db():
    if not firebase_admin._apps:
        cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if not cred_json:
            raise Exception("FIREBASE_CREDENTIALS not set")
        cred = credentials.Certificate(json.loads(cred_json))
        firebase_admin.initialize_app(cred)
    return firestore.client()
