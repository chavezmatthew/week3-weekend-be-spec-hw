from flask import request, jsonify
from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select


#Create Mechanic
@mechanics_bp.route("/", methods = ['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201

#Retrieve Mechanics
@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200

#Retrieve Mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    return mechanic_schema.jsonify(mechanic), 200

#Update Mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic == None:
        return jsonify({"Message": "Invalid id"}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in mechanic_data.items():
        if value:
            setattr(mechanic, field, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#Delete Mechanic
@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic == None:
        return jsonify({"Message": "Invalid id"}), 400
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted mechanic {mechanic_id}!"})
