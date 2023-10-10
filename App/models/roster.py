from App.database import db

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('regularuser.id'), nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    regularuser = db.relationship('RegularUser', back_populates='competitions')
    competition = db.relationship('Competition', back_populates='users')