from asyncio import Task
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os 
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate('src/SecretKey.json')
firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('DB_URL')
    })

def getDBReference(refof):
    ref = db.reference(refof)
    print(ref.get())
    return ref
