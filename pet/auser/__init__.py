# Registered User Access Blueprint

from flask import Blueprint, abort

main = Blueprint('main', __name__, template_folder='templates')

from pet.auser.views import *