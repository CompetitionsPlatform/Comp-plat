from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import get_all_comps

comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

@comp_views.route('/competitions', methods=['GET'])
def comp_page():
    comps = get_all_comps
    if comps:
        return jsonify(comps), 200
    else:
        return jsonify("error": "no competitions found"), 204
    
