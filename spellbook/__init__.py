import sys
from flask import Flask, request, url_for, render_template, abort, redirect
import flask_login
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///dnd.db?check_same_thread=False',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False,
    TESTING = False
))

app.config.from_envvar('SPELLBOOK_SETTINGS', silent=True)
app.jinja_env.add_extension('jinja2.ext.do')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
from spellbook.models import User

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'not a chance'

@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)

@login_manager.request_loader
def request_loader(request):
    uname = request.form.get('uname')
    if uname != None:
        user = User.query.get(uname)
        if user == None:
            return
    else:
        return

    user = User()
    user.id = name
    return user

from spellbook.views_spell import page_not_found, home, spells_by_level, spell_details
from spellbook.views_auth import profile, logout, register, login
from spellbook.helpers import *

#Context Processors
@app.context_processor
def processors():
    return dict(get_schools=get_schools,get_baseclasses=get_baseclasses,getBaseClassID=getBaseClassID,get_subclasses=get_subclasses,getClassName=getClassName,getDescriptionForKeyValue=getDescriptionForKeyValue,getXHeaderID=getXHeaderID, getYesNo=getYesNo, getLevelTitle=getLevelTitle, getUser=getUser, isMySpell=isMySpell, isMyUser=isMyUser)