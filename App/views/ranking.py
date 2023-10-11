from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import *

rankingviews = Blueprint('ranking_views', __name__, template_folder='../templates')

@ranking_views.route('/ranking', methods=['GET'])
def get_ranked():
    users = RegularUser.query.order_by(RegularUser.rank.desc()).limit(20).all()
    top20 = []
    
    if users:
        for user in users:
        top20.append(user.toJSON_brief())
