from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, BourbonWhiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Creating a new whiskey 
@api.route('/whiskey', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    style = request.json['style']
    name= request.json['name']
    abv = request.json['abv']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'Test: {current_user_token.token}')

    whiskey = BourbonWhiskey(style, name, year, abv, user_token = user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskeys', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_whiskey = current_user_token.token
    whiskeys = BourbonWhiskey.query.filter_by(user_token = a_whiskey).all()
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)


#Updating whiskey
@api.route('whiskeys/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = BourbonWhiskey.query.get(id)
    whiskey.style = request.json['style']
    whiskey.name = request.json['name']
    whiskey.year = request.json['year']
    whiskey.abv = request.json['abv']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

# Delete the whiskey
@api.route('/whiskeys/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = BourbonWhiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)