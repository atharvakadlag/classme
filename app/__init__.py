from flask import Flask

app = Flask(__name__)
app.secret_key = 'my super secret key' # TODO: change this to something more secretive

from app import routes
