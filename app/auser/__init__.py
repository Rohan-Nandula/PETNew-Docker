from flask import Blueprint

auser = Blueprint('auser', __name__)

from . import views
from . import models