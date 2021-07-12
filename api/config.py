from dotenv import load_dotenv
from os import path,environ

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR,'.env'))

class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    TESTING = False
    
class Development(Config):
    DEBUG = True
    MONGO_URI = environ.get("MONGO_URI")
    ENV = "development"

class Production(Config):
    DEBUG  = False
    MONGO_URI = environ.get("MONGO_URI")
    ENV = 'production'
