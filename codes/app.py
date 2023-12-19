from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'sfhiybbcuenkhyibkjcksadhflkdflkjd'
# app.config['SESSION_TYPE'] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery_.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

from admin import *
from user import *
from grocery import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
