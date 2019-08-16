from spellbook import app, db
import flask_login
from flask import redirect, render_template, url_for, request, jsonify, session, abort
from spellbook.models import User, spells, user_spells
from spellbook.helpers import getUser
from spellbook.views_spell import get_entries
from urllib.parse import urlparse, urljoin, urlencode, parse_qsl, urlunparse

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    error='Something unexpected happened.'

    uname = request.form['uname']
    user = User.query.filter_by(name=uname).first()
    if user != None:
        if user.check_password(request.form['pw']):
            flask_login.login_user(user, remember=True)
            next = request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(404)

            return redirect(next or url_for('spells_by_level'))
        else:
            error="wrong password"
    else:
        error="username not found"

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    uname = request.form['uname']
    if User.query.filter_by(name=uname).first() != None:
        error='username taken'
        return render_template('register.html', error=error)

    pw = request.form['pw']
    pw2 = request.form['pw2']
    if pw == "" or pw2 == "":
        error='passwords cannot be blank'
        return render_template('register.html', error=error)

    if pw != pw2:
        error='passwords need to match'
        return render_template('register.html', error=error)

    user = User(username=uname, password=pw)
    db.session.add(user)
    db.session.commit()
    flask_login.login_user(user, remember=True)
    return redirect(url_for('spells_by_level'))

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('spells_by_level'))

@app.route('/profile')
def profile():
    useridarg = request.args.get('uid', None)
    if useridarg == None:
        return redirect(url_for('profile', uid=getUser().id))

    return render_template('profile.html', levels=range(0,10), entries=get_entries(request.args))

@app.route('/printable')
def printable():
    useridarg = request.args.get('uid', None)
    if useridarg == None:
        return redirect(url_for('printable', uid=getUser().id))

    return render_template('printable.html', levels=range(0,10), entries=get_entries(request.args))

@app.route('/profiles')
def profilelist():
    return render_template('profilelist.html', users=User.query.order_by("id").all())

@app.route('/addspell/<int:spellid>', methods=['GET'])
@flask_login.login_required
def addspell(spellid):
    spellrec = spells.query.get(spellid)
    if  spellrec != None:
        if user_spells.query.filter_by(userID=getUser().id).filter_by(spellID=spellid).first() == None:
            rec = user_spells()
            rec.userID = getUser().id
            rec.spellID = spellid
            db.session.add(rec)
            db.session.commit()
        else:
            return jsonify({'data': render_template('spell_list_items_entry.html', entry=spellrec)})
    else:
        return jsonify({'data': "Spell does not exist"})
    
    next = request.args.get('next', None)
    if next != None:
        if not is_safe_url(next):
            return flask.abort(404)
        else:
            return redirect(next)

    return jsonify({'data': render_template('spell_list_items_entry.html', entry=spellrec)})

@app.route('/removespell/<int:spellid>', methods=['GET'])
@flask_login.login_required
def removespell(spellid):
    spellrec = spells.query.get(spellid)
    if spellrec != None:
        rec = user_spells.query.filter_by(userID=getUser().id).filter_by(spellID=spellid).first()
        if  rec != None:
            db.session.delete(rec)
            db.session.commit()
        else:
            return jsonify({'data': render_template('spell_list_items_entry.html', entry=spellrec)})
    else:
        return jsonify({'data': "Spell does not exist"})

    next = request.args.get('next', None)
    if next != None:
        if not is_safe_url(next):
            return flask.abort(404)
        else:
            return redirect(next)

    return jsonify({'data': render_template('spell_list_items_entry.html', entry=spellrec)})