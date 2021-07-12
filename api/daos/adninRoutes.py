from flask import Blueprint,request,jsonify,session
from passlib.hash import pbkdf2_sha256
from os import environ
from .notification_daos import Datadaos
import datetime
import uuid
import jwt
def create_blueprint(cluster):
    adnin = Blueprint("adnin",__name__,url_prefix="/k")
    daos = Datadaos(cluster)

    @adnin.route("/c/i/p/h/e/r/a/c/c/e/s/s",methods=['GET','POST'])      
    def cipher_access():
        if request.method == 'POST':
            username = request.json["username"]
            password = request.json["password"]
            hashed_pass = pbkdf2_sha256.hash(password)
            response = cluster.db.admins.insert_one({
                "username" : username, 
                "password" : hashed_pass,
                "admin_id": str(uuid.uuid4())
            })
            if response:
                jwt_encoded = jwt.encode({"username" : username, "exp" : datetime.datetime.utcnow()+datetime.timedelta(days=1)},environ.get("SECRET_KEY"))
                session["token"] = jwt_encoded
                return jsonify({"status" : 200,"token" : str(jwt_encoded)})
            return jsonify({"status" : 400,"message" : "Operation Failed"})

    return adnin