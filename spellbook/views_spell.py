from spellbook import app
from spellbook.models import spells, classes, spell_schools, spell_class_ref, User, user_spells
from flask import redirect, render_template, url_for, request, jsonify, abort
from spellbook.helpers import getUser
from spellbook.globals import feature_list
from urllib import request as librequest
import re

def get_entries(requestargs):
    entries=spells.query

    text = requestargs.get('name', None)
    if text is not None:
        text = librequest.unquote(text)
        text = re.sub(r"[^\w\d'\s]+",'', text)
        for s in text.split():
            entries = entries.filter(spells.name.ilike("%"+s+"%"))

    cs = requestargs.get('cs', None)
    if cs is not None:
        entries = entries.join(spell_class_ref).filter(spell_class_ref.classID == cs)

    sch = requestargs.get('sch', None)
    if sch is not None:
        rec = spell_schools.query.get(sch)
        if rec is None:
            abort(404, "school not found")
        school = rec.name
        entries = entries.filter(spells.school == school)

    lvl = requestargs.get('lvl', None)
    if lvl is not None:
        local_levels = (int(lvl),)
        if int(lvl)>9 or int(lvl)<0:
            abort(404, "level not valid")
        entries = entries.filter(spells.level == str(lvl))
    
    rit = requestargs.get('rit', None)
    if rit is not None:
        if int(rit) is 0:
            rit = 0
        else:
            rit = 1
        entries = entries.filter(spells.ritual == rit)

    conc = requestargs.get('conc', None)
    if conc is not None:
        if int(conc) is 0:
            conc = 0
        else:
            conc = 1
        entries = entries.filter(spells.concentration == conc)

    verbal = requestargs.get('ver', None)
    if verbal is not None:
        if int(verbal) is 0:
            verbal = 0
        else:
            verbal = 1
        entries = entries.filter(spells.verbal == verbal)

    somatic = requestargs.get('som', None)
    if somatic is not None:
        if int(somatic) is 0:
            somatic = 0
        else:
            somatic = 1
        entries = entries.filter(spells.somatic == somatic)

    material = requestargs.get('mat', None)
    if material is not None:
        if int(material) is 0:
            material = 0
        else:
            material = 1
        entries = entries.filter(spells.material == material)

    uid = requestargs.get('uid', None)
    if uid is not None:
        rec = User.query.get(uid)
        if rec is None:
            abort(404, "user not found")
        entries = entries.join(user_spells).filter(user_spells.userID == rec.id)
         
    return entries.order_by('level').order_by('name')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=e.description)

@app.route('/')
def home():
    return render_template('home.html', entries=get_entries(request.args).all())

@app.route('/about')
def about():
    return render_template('welcome.html', features=feature_list)

@app.route('/spells', methods=['GET'])
def spells_by_level():
    return render_template('home.html', entries=get_entries(request.args).all())

@app.route('/spellfilter', methods=['GET'])
def spellfilter():
    return jsonify({'data': render_template('spell_list.html', entries=get_entries(request.args))})

@app.route('/spellfilternav', methods=['GET'])
def spellfilternav():
    return jsonify({'data': render_template('spellnav.html')})

@app.route('/spell/<int:id>')
def spell_details(id):
    return render_template('spell_details.html', spell=spells.query.get_or_404(id))
