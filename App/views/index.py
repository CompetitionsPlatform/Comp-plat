from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.controllers import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    
    usr = create_admin('ronel', 'pseudo')

    ruser1 = create_regular_user('cusr1', '1234')
    ruser2 = create_regular_user('cusr2', 'ronel')
    ruser3 = create_regular_user('cusr3', 'ronel')

    comp = create_competition(usr.id, 'comp1', 'details 1', datetime.utcnow())
    comp2 = create_competition(usr.id, 'comp2', 'details 5', datetime.utcnow())

    toggle_registration(ruser1.id, comp.id)
    toggle_registration(ruser1.id, comp2.id)
    
    
    temp = login(usr.username, 'pseudo')

    new_result = create_result(comp.id, ruser3.id, 99.9)
    
    if new_result:
        return jsonify(ruser3.toJSON())
    else:
        return ('error')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})