import sqlite3
import xml.etree.ElementTree as ET

#SQL
conn = sqlite3.connect('../dnd.db')
cursor = conn.cursor()

with open('schema.sql', mode='r') as f:
    cursor.executescript(f.read())
conn.commit()

#XML
tree = ET.parse('spells.xml')
root = tree.getroot()

#spell schools
spell_schools = {"A":"Abjuration",
                 "C":"Conjuration",
                 "D":"Divination",
                 "EN":"Enchantment",
                 "EV":"Evocation",
                 "I":"Illusion",
                 "N":"Necromancy",
                 "T":"Transmutation"}

#for c in spell_schools.values():
#    cursor.execute('insert into spell_schools(name) values(?)', (c,))

#classes
classes_record = {}

for spell in root.findall("spell"):
    duration = spell.find('duration').text
    classes = spell.find('classes').text
    classids = []
    
    for c in classes.split(', '):
        subclass = None
        if (c.find('(') is not -1) and (c[:7] != "Fighter") and (c[:5] != "Rogue"):
            #c is a subclass - change vars
            subclass = c[c.index("(")+1 : c.rindex(")")]
            c = c[:c.find(' (')]
            
        if c not in classes_record.keys():
            #c is a base class
            cursor.execute('insert into classes(name, isSubclassFor) values(?, ?)', (c,0))
            classes_record[c] = cursor.lastrowid
        
        if subclass is not None:
            if subclass not in classes_record.keys():
                cursor.execute('insert into classes(name, isSubclassFor) values(?, ?)', (subclass,classes_record[c]))
                classes_record[subclass] = cursor.lastrowid
            classids.append(classes_record[subclass])
        else:
            classids.append(classes_record[c])

    text = ""
    for line in spell.findall('text'):
        if line.text is not None:
            text = text+line.text+"<br />"
        else:
            text = text+"<br />"
    
    verbal = False
    somatic = False
    material = False

    components = spell.find('components').text.strip()

    for strs in components.split(','):
        s = strs.strip()[0]
        if s == "V":
            verbal = True
        elif s == "S":
            somatic = True
        elif s == "M":
            material = True

    spell_record = (spell.find('name').text.strip(), 
                     spell.find('level').text,
                     spell_schools[spell.find('school').text].strip(),
                     spell.find('time').text.strip(),
                     spell.find('range').text.strip(),
                     components,
                     duration,
                     (duration.lower().find('concentration') >= 0),
                     spell.find('ritual') is not None,
                     verbal,
                     somatic,
                     material,
					 classes,
                     text)

    cursor.execute('''insert into spells(name, level, school, cast_time, range_, components, duration, concentration, ritual, verbal, somatic, material, classes, descrip) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', spell_record)

    spellID = cursor.lastrowid
    for classID in classids:
        try:
            cursor.execute('insert into spell_class_ref(spellID, classID) values(?, ?)', (spellID, classID))
        except:
            continue

conn.commit()
