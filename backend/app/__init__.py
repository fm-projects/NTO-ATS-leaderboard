from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder="../dist/static", template_folder="../dist")

from app import views
