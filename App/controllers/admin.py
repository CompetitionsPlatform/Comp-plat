from App.database import db
from App.models import Admin

def create_admin(username, password):
    newadmin = Admin(username=username, password=password)
    try:
        db.session.add(newadmin)
        db.session.commit()
        return newadmin
    except:
        return None
    
def is_admin(admin_id):
    admin = Admin.query.filter_by(id=admin_id).first()
    return admin is not None