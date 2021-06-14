# User authentication blueprint

from flask import Blueprint, abort

auth = Blueprint('auth', __name__, template_folder='templates')

from pet.auth.views import *
