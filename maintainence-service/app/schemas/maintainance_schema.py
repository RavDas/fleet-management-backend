from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date

class MaintenanceItemSchema(Schema):
    id = fields.Str(required=True)
    vehicle = fields.Str(required=True, data_key='vehicle')
    type = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str(
        required=True,
        validate=validate.OneOf(['overdue', 'due_soon', 'scheduled', 'in_progress', 'completed', 'cancelled'])
    )
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(['low', 'medium', 'high', 'critical'])
    )
    dueDate = fields.Date(required=True)
    scheduledDate = fields.DateTime()
    completedDate = fields.DateTime()
    currentMileage = fields.Int(required=True)
    dueMileage = fields.Int(required=True)
    cost = fields.Float()
    actualCost = fields.Float()
    assignedTo = fields.Str()
    assignedTechnician = fields.Str()
    notes = fields.Str()
    partsNeeded = fields.List(fields.Dict())
    attachments = fields.List(fields.Dict())
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)

class MaintenanceItemCreateSchema(Schema):
    vehicle = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    type = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(['low', 'medium', 'high', 'critical'])
    )
    dueDate = fields.Date(required=True)
    currentMileage = fields.Int(required=True, validate=validate.Range(min=0))
    dueMileage = fields.Int(required=True, validate=validate.Range(min=0))
    cost = fields.Float(validate=validate.Range(min=0))
    assignedTo = fields.Str()
    notes = fields.Str()
    partsNeeded = fields.List(fields.Dict())
    
    @validates('dueMileage')
    def validate_due_mileage(self, value):
        if 'currentMileage' in self.context and value < self.context['currentMileage']:
            raise ValidationError('Due mileage must be greater than current mileage')

class MaintenanceItemUpdateSchema(Schema):
    type = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str()
    status = fields.Str(
        validate=validate.OneOf(['overdue', 'due_soon', 'scheduled', 'in_progress', 'completed', 'cancelled'])
    )
    priority = fields.Str(
        validate=validate.OneOf(['low', 'medium', 'high', 'critical'])
    )
    dueDate = fields.Date()
    scheduledDate = fields.DateTime()
    currentMileage = fields.Int(validate=validate.Range(min=0))
    dueMileage = fields.Int(validate=validate.Range(min=0))
    cost = fields.Float(validate=validate.Range(min=0))
    actualCost = fields.Float(validate=validate.Range(min=0))
    assignedTo = fields.Str()
    assignedTechnician = fields.Str()
    notes = fields.Str()
    partsNeeded = fields.List(fields.Dict())
    attachments = fields.List(fields.Dict())