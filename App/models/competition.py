from App.database import db
from datetime import datetime

class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False, unique=True)
    details = db.Column(db.String(400), nullable=False)
    score_max = db.Column(db.Float, nullable=False, default=100.0)
    event_date = db.Column(db.DateTime, default=datetime.utcnow())
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    admin = db.relationship('Admin', back_populates='competitions')
    users = db.relationship('Roster', back_populates='competition', lazy='joined')
    results = db.relationship('Result', back_populates='competition')


    # owner (admin)
    def __init__(self,admin_id,  name, details, date):
        self.admin_id = admin_id
        self.name = name
        self.details = details
        self.event_date = date
        self.score_max = 100.0

    def __repr__(self):
        return f'{self.name} {self.details}'

    def toJSON_brief(self):
        return {
            'comp_id': self.id,
            'comp_name': self.name,
            'comp_details': self.details,
            'comp_date': self.event_date,
            'comp_admin': self.admin.username,
        }

    def toJSON(self):
        result_list = []
        
        for result in self.results:
            if result:
                result_info = result.toJSON()
                result_list.append(result_info)

        user_list = []
        for user in self.users:
            if user:
                # Access user information through the Roster relationship
                user_info = {
                    'user_id': user.regularuser.id,
                    'username': user.regularuser.username,
                    'rank': user.regularuser.rank,
                    'overall': user.regularuser.overall,
                }
                user_list.append(user_info)

        return {
            'comp_id': self.id,
            'comp_name': self.name,
            'comp_details': self.details,
            'comp_date': self.event_date,
            'comp_admin': self.admin.username,
            'results': result_list,
            'registered_users': user_list,
        }