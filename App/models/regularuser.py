from App.database import db
from .user import User
from .competition import Competition

class RegularUser(User):
    __tablename__ = 'regularuser'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    rank = db.Column(db.Integer, nullable=False, default=0)
    overall = db.Column(db.Float, nullable=False, default=0.0)
    competitions = db.relationship('Roster', back_populates='regularuser', lazy='joined')
    results = db.relationship('Result', back_populates='regularuser')

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rank = 0
        self.overall = 0.0

    def toJSON_brief(self):
        return{
            'user_id': self.id,
            'username': self.username,
            'rank': self.rank
        }

    def toJSON(self):
        competition_list = []

        for roster in self.competitions:
            comp = roster.competition
            if comp:
                comp_info = comp.toJSON()
                competition_list.append(comp_info)
        
        result_list = []
        
        for result in self.results:
            if result:
                result_info = result.toJSON()
                result_list.append(result_info)

        user_json = {
            'user_id': self.id,
            'username': self.username,
            'rank': self.rank,
            'competitions': competition_list,
            'user_results': result_list
        }

        return user_json