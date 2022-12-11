from flask import Flask

app = Flask(
    __name__,
    static_folder="../dist/static",
    template_folder="../dist"
)

from app import views
