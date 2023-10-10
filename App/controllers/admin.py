from App.database import db
from .user import User

class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    competitions = db.relationship('Competition', back_populates='admin')
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def toJSON(self):
        competition_list = []

        for comp in self.competitions:
            if comp:
                comp_info = comp.toJSON()
                competition_list.append(comp_info)

        return {
            'admin_id': self.id,
            'username': self.username,
            'admin_comps': competition_list
        }
