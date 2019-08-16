from spellbook import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.name = username
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, passw):
        return check_password_hash(self.password, passw)

    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False

class spells(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text)
    level =  db.Column(db.Integer)
    school = db.Column(db.Text)
    cast_time = db.Column(db.Text)
    range_ = db.Column(db.Text)
    components = db.Column(db.Text)
    duration = db.Column(db.Text)
    concentration = db.Column(db.Boolean)
    ritual = db.Column(db.Boolean)
    verbal = db.Column(db.Boolean)
    somatic = db.Column(db.Boolean)
    material = db.Column(db.Boolean)
    classes = db.Column(db.Text)
    descrip = db.Column(db.Text)

class classes(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text)
    isSubClassFor = db.Column(db.Integer)
    
class spell_schools(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text)

class spell_class_ref(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    spellID = db.Column(db.Integer, db.ForeignKey("spells.id"))
    classID = db.Column(db.Integer, db.ForeignKey("classes.id"))

class user_spells(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"))
    spellID = db.Column(db.Integer, db.ForeignKey("spells.id"))