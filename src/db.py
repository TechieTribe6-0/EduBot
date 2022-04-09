import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os 
from dotenv import load_dotenv
load_dotenv()

# Fetch the service account key JSON file contents
cred = credentials.Certificate('SecretKey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('DB_URL')
})

ref = db.reference('')
print(ref.get())
