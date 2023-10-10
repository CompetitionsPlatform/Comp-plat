from App.database import db

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False, default=0.0)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('regularuser.id'), nullable=False)
    regularuser = db.relationship('RegularUser', back_populates='results')
    competition = db.relationship('Competition', back_populates='results')
    
    def __init__(self, comp_id, user_id, score):
        self.comp_id = comp_id
        self.user_id = user_id
        self.score = score
    
    def toJSON(self):
        return {
            'comp_id': self.comp_id,
            'user_id': self.user_id,
            'score': self.score,
        }