from flask import request, jsonify
from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from marshmallow import ValidationError
from app.models import ServiceTicket, Mechanic, db
from sqlalchemy import select
from datetime import datetime


#Create Service Ticket
@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        new_service_ticket = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if not new_service_ticket.service_date:
        new_service_ticket.service_date = datetime.now()

    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201

#Retrieve Service Tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets), 200

#Retrieve Service Ticket
@service_tickets_bp.route("/<int:service_ticket_id>", methods=["GET"])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    return service_ticket_schema.jsonify(service_ticket), 200

#Update Service Ticket
@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket is None:
        return jsonify({"Message": "Invalid id"}), 400
    
    try:
        service_ticket_schema.load(request.json, instance=service_ticket, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#Update Mechanic to Service Ticket
@service_tickets_bp.route("/<int:ticket_id>/add_mechanic/<int:mechanic_id>", methods=['PUT'])
def add_mechanic_to_service_ticket(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    if not service_ticket:
        return jsonify({"Message": "Service ticket not found"}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"Message": "Mechanic not found"}), 404

    if mechanic not in service_ticket.mechanics:
        service_ticket.mechanics.append(mechanic)
        db.session.commit()
        return jsonify({"Message": f"Mechanic {mechanic_id} added to service ticket {ticket_id}"}), 200
    else:
        return jsonify({"Message": "Mechanic is already assigned to this service ticket"}), 400

#Delete Service Ticket
@service_tickets_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket == None:
        return jsonify({"Message": "Invalid id"}), 400
    
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted service_ticket {service_ticket_id}!"})
