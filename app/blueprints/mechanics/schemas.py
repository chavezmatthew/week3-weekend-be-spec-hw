from app.models import Mechanic
from app.extensions import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_relationships = True
        load_instance = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many = True)