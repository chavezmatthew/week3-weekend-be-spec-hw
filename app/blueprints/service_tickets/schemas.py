from app.models import ServiceTicket
from app.extensions import ma
from app.blueprints.mechanics.schemas import MechanicSchema
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = True

    mechanics = ma.List(ma.Nested(MechanicSchema))
    service_date = fields.Date(required=False)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many = True)