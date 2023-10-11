from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user
from App.controllers import *

profile_views = Blueprint('profile_views', __name__, template_folder='../templates')

@profile_views.route('/profiles/<int:id>', methods=['GET'])
def get_profile_page(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.toJSON()), 200
    else:
        return jsonify({"error" : "user does not exist"}), 404
