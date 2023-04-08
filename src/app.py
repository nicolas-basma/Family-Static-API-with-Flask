"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def all_family_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members)


@app.route('/members', methods=['POST'])
def create_member():
    new_member = request.json
    add_member = {
        "firt_name": new_member["first_name"],
        "age": new_member["age"],
        "lucky_numbers": new_member["lucky_numbers"],
        "id": new_member["id"]
    }
    members = jackson_family.add_member(add_member)
    return jsonify(members), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def remove_member(member_id):
    members_filtered = jackson_family.delete_member(member_id)
    return jsonify(members_filtered)

@app.route('/member/<int:member_id>', methods=['GET'])
def select_member(member_id):
    member_selected = jackson_family.get_member(member_id)
    return jsonify(member_selected)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
