from flask import Flask

import os
from flask_bcrypt import Bcrypt

app= Flask(__name__)

bcrypt = Bcrypt(app)


from application import routes