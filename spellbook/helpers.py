from spellbook.models import spells, classes, spell_schools, spell_class_ref, User, user_spells
import flask_login

levels_english = {
    "0": "Cantrips",
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine"
}

def getDescriptionForKeyValue(key, value):
    funcMap = {
        'sch' : getSchoolName,
        'cs'  : getClassName,
        'lvl' : getLevelTitle,
        'rit' : getRitualString,
        'conc': getConcentrationString,
        'ver' : getVerbalString,
        'som' : getSomaticString,
        'mat' : getMaterialString
    }
    if key in funcMap:
        return funcMap[key](value)
    return None

def getSchoolName(schid):
        return spell_schools.query.get_or_404(schid).name

def getClassName(csid):
    subclass = classes.query.get(csid)
    if subclass is None:
        abort(404, "class or subclass not found")
    name = subclass.name
    if subclass.isSubClassFor != 0:
        name = classes.query.get(subclass.isSubClassFor).name + " (" + name + ")"
    return name

def getLevelTitle(lvl, addTitle=True):
    if addTitle:
        if lvl == "0":
            return "Cantrips"
        return "Level "+levels_english[str(lvl)]
    return levels_english[str(lvl)]

def getRitualString(value):
    return "Ritual: "+getYesNo(value)

def getConcentrationString(value):
    return "Concentration: "+getYesNo(value)

def getVerbalString(value):
    return "Verbal: "+getYesNo(value)

def getSomaticString(value):
    return "Somatic: "+getYesNo(value)

def getMaterialString(value):
    return "Material: "+getYesNo(value)

def getYesNo(val):
    return "Yes" if int(val)==1 else "No"

def getXHeaderID(key, value):
    funcMap = {
        'cs'  : getBaseClassID
    }
    if key in funcMap:
        return funcMap[key](value)
    return None

def getBaseClassID(scid):
    ret = classes.query.get(scid).isSubClassFor
    return ret if ret != 0 else None

def get_schools():
    l = []
    for s in spell_schools.query.order_by('name').all():
        l.append(str(s.id))
    return l

def get_baseclasses():
        return classes.query.filter(classes.isSubClassFor==0).order_by('name').all()

def get_subclasses(baseclassid):
        if baseclassid is None:
            baseclassid = 0
        return classes.query.filter(classes.isSubClassFor==baseclassid).order_by('name').all()

def getUser(uid=None):
    if uid == None:
        uid = flask_login.current_user.get_id()

    if uid != None:
        return User.query.get(uid)
    
    return None

def isMyUser(uid):
    if flask_login.current_user.get_id() == None:
        return False
        
    return (int(flask_login.current_user.get_id()) == int(uid))

def isMySpell(spellid):
    user = getUser()
    if user == None:
        return False
    return user_spells.query.filter_by(userID=user.id).filter_by(spellID=spellid).first() != None