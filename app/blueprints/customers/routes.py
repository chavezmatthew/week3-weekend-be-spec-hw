from flask import request, jsonify
from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select


#Create Customer
@customers_bp.route("/", methods = ['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

#Retrieve Customers
@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers), 200

#Retrieve Customer
@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    return customer_schema.jsonify(customer), 200

#Update Customer
@customers_bp.route("/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({"Message": "Invalid id"}), 400
    
    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        if value:
            setattr(customer, field, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#Delete Customer
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({"Message": "Invalid id"}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"Message": f"Successfully deleted customer {customer_id}!"})
