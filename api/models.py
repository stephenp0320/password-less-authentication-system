from api import db

class Item(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)

    def  __repr__(self):
        return '<Item %r>' % self.name