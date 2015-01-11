from peewee import *

dbproxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = dbproxy

class Cards(BaseModel):
    data = TextField()
    did = IntegerField()
    due = IntegerField()
    factor = IntegerField()
    flags = IntegerField()
    ivl = IntegerField()
    lapses = IntegerField()
    left = IntegerField()
    mod = IntegerField()
    nid = IntegerField(index=True)
    odid = IntegerField()
    odue = IntegerField()
    ord = IntegerField()
    queue = IntegerField()
    reps = IntegerField()
    type = IntegerField()
    usn = IntegerField(index=True)

    class Meta:
        db_table = 'cards'

class Col(BaseModel):
    conf = TextField()
    crt = IntegerField()
    dconf = TextField()
    decks = TextField()
    dty = IntegerField()
    ls = IntegerField()
    mod = IntegerField()
    models = TextField()
    scm = IntegerField()
    tags = TextField()
    usn = IntegerField()
    ver = IntegerField()

    class Meta:
        db_table = 'col'

class Graves(BaseModel):
    oid = IntegerField()
    type = IntegerField()
    usn = IntegerField()

    class Meta:
        db_table = 'graves'

class Notes(BaseModel):
    csum = IntegerField(index=True)
    data = TextField()
    flags = IntegerField()
    flds = TextField()
    guid = TextField()
    mid = IntegerField()
    mod = IntegerField()
    sfld = IntegerField()
    tags = TextField()
    usn = IntegerField(index=True)

    class Meta:
        db_table = 'notes'

class Revlog(BaseModel):
    cid = IntegerField(index=True)
    ease = IntegerField()
    factor = IntegerField()
    ivl = IntegerField()
    lastivl = IntegerField(db_column='lastIvl')
    time = IntegerField()
    type = IntegerField()
    usn = IntegerField(index=True)

    class Meta:
        db_table = 'revlog'