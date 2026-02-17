import os
import firebase_admin
from firebase_admin import credentials, firestore

# This will point to the JSON created in GitHub Actions
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

