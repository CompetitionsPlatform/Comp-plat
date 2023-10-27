from App.database import db
from App.models import Competition
from App.models import Result
from App.models import RegularUser
from App.controllers import is_admin, is_user
from datetime import datetime

def get_comp_by_id(comp_id):
    comp = Competition.query.filter_by(id=comp_id).first()
    if comp:
        return comp
    else:
        return None
    
def create_competition(admin_id, name, details, date):
    if is_admin(admin_id):
        try:
            event_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
            new_competition = Competition(admin_id, name, details, event_date)
            db.session.add(new_competition)
            db.session.commit()
            return new_competition
        except Exception as e:
            print("Error creating competition")
            db.session.rollback()
            return None
    return None

def is_competition(comp_name):
    comp = Competition.query.filter_by(name=comp_name).first()
    if comp:
        return comp
    else:
        return None

def delete_competition(comp_id):
    comp = get_comp_by_id(comp_id)
    if comp:
        try:
            db.session.remove(comp)
            db.session.commit()
            return comp
        except:
            return None
    else:
        return None

def get_all_comps():
    competition_list = []
    comps = Competition.query.all()
    if comps:
        return comps
    else:
        return None
    return None

def get_ranked():
    users = RegularUser.query.order_by(RegularUser.rank.desc()).limit(20).all()
    return users
    
def create_result(comp_id, user_id, score):
    if is_user(user_id):
        new_result = Result(comp_id, user_id, score)
        try:
            db.session.add(new_result)
            db.session.commit()
            return new_result
        except:
            return None

def update_result(new_result):
    pass

def create_results():
    pass