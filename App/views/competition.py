from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from flask_login import current_user
from App.controllers import get_all_comps, get_comp_by_id, is_admin, create_competition, is_competition, delete_competition

comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

@comp_views.route('/competitions', methods=['GET'])
def competitions_page():
    competition_list = []
    comps = get_all_comps()
    if comps:
        for comp in comps:
            competition_list.append(comp.toJSON_brief())
            return jsonify(competition_list), 200
    else:
        return jsonify({"error": "no competitions found"}), 202

@comp_views.route('/competitions/<int:id>', methods=['GET'])
def competition_detail_page(id):
    comp = get_comp_by_id(id);
    if comp:
        return jsonify(comp.toJSON())

@comp_views.route('/competitions', methods=['GET'])
def competitions_page_create():
    data = request.json
    user = current_user
    if user:
        if is_admin(user.id):
            comp = is_competition(date['name'])
            if not comp:
                comp = create_competition(user.id, data['name'], data['details'], data['date'])
                if comp:
                    return jsonify({"success" : "competition created"}), 200
                else:
                    return jsonify({"error" : "bad request"}), 400
            else:
                return jsonify({"error" : "competition with that name already exists"}), 400
    return jsonify({"error" : "unauthorized"}), 401

@comp_views.route('/competitions/<int:id>', methods=['DELETE'])
def competition_detail_page_delete(id):
    comp = delete_competition(id)
    if comp:
        return jsonify({"success": "competition deleted"}), 200
    else:
        return jsonif({"error": "cannot process request"}), 400

     
