from flask import Flask
import configparser
import logging

logging.basicConfig(filename='elefant.log', level=logging.DEBUG)

config = configparser.ConfigParser(interpolation=None)
config.read("conf/app.conf")

app = Flask(__name__,
            static_url_path='')
app.config['SECRET_KEY'] = config['cryptography']['SecretKey']
app.config['BASIC_AUTH_USERNAME'] = config['auth']['User']
app.config['BASIC_AUTH_PASSWORD'] = config['auth']['Password']

from app import routes
