from flask import Flask, Blueprint,jsonify
from flask_cors import CORS
from os import environ
from api.daos import adninRoutes
from . import config
from flask_pymongo import PyMongo
from .routes import dataRoutes, adminRoutes


def create_app():
    app = Flask(__name__)
    cors = CORS(app, origins='*')
    app.config.from_object(environ.get("CONFIG_FROM",config.Development()))
    cluster = PyMongo(app)


    app.register_blueprint(dataRoutes.create_blueprint(cluster))
    app.register_blueprint(adninRoutes.create_blueprint(cluster))
    app.register_blueprint(adminRoutes.create_blueprint(cluster))
    
    # @app.route("/",methods = ["GET"])
    # def status():
    #     return jsonify({"status" : "app is running"})

    return app

