# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

from . import cli
from . import routes
