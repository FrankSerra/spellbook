drop table if exists spells;
create table spells (
    id integer primary key autoincrement,
    name text not null,
    level integer,
    school text,
    cast_time text,
    range_ text,
    components text,
    duration text not null,
    concentration boolean,
	ritual boolean,
    verbal boolean,
    somatic boolean,
    material boolean,
    classes text,
    subclasses text,
    descrip text not null
);

drop table if exists classes;
create table classes (
    id integer not null primary key,
    name text not null,
    isSubclassFor integer
);

drop table if exists spell_class_ref;
create table spell_class_ref (
    id integer not null primary key,
    spellID integer not null,
    classID integer not null,
    foreign key(spellID) references spells(id),
    foreign key(classID) references classes(id),
	unique(spellID, classID)
);

/*drop table if exists spell_schools;
create table spell_schools (
    id integer not null primary key,
    name text not null    
);

drop table if exists users;
create table users (
	id integer not null primary key,
    name text not null,
    password text not null
);

drop table if exists user_spells;
create table user_spells (
	id integer not null primary key,
	userID integer not null,
	spellID integer not null,
	foreign key(userID) references users(id),
	foreign key(spellID) references spells(id),
	unique(userID, spellID)
);*/