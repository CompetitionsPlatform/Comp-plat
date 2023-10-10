from App.models import RegularUser
from App.database import db

#remove
from App.models import *

def create_regular_user(username, password):
    newuser = RegularUser(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def is_user(user_id):
    user = RegularUser.query.filter_by(id=user_id).first()
    return user is not None

def get_user_by_id(user_id):


def toggle_registration(user_id, comp_id):
    existing_registration = Roster.query.filter_by(user_id=user_id, comp_id=comp_id).first()

    if existing_registration:
        try:
            db.session.delete(existing_registration)
            db.session.commit()
            return None
        except:
            print('Error removing registration')
            db.session.rollback()
            return None
    else:
        new_registration = Roster(user_id=user_id, comp_id=comp_id)
        try:
            db.session.add(new_registration)
            db.session.commit()
            return new_registration
        except:
            print('Error registering user')
            db.session.rollback()
            return None