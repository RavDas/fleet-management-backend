from app import db
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY

class MaintenanceStatus(str, Enum):
    OVERDUE = 'overdue'
    DUE_SOON = 'due_soon'
    SCHEDULED = 'scheduled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class MaintenancePriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

class TechnicianStatus(str, Enum):
    AVAILABLE = 'available'
    BUSY = 'busy'
    OFF_DUTY = 'off-duty'

class FrequencyType(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'
    MILEAGE_BASED = 'mileage-based'

class MaintenanceItem(db.Model):
    __tablename__ = 'maintenance_items'
    
    id = db.Column(db.String(50), primary_key=True)
    vehicle_id = db.Column(db.String(50), nullable=False, index=True)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(MaintenanceStatus, name='maintenancestatus', values_callable=lambda x: [e.value for e in x]), default=MaintenanceStatus.SCHEDULED, nullable=False)
    priority = db.Column(db.Enum(MaintenancePriority, name='maintenancepriority', values_callable=lambda x: [e.value for e in x]), default=MaintenancePriority.MEDIUM, nullable=False)
    
    # Dates
    due_date = db.Column(db.Date, nullable=False)
    scheduled_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Mileage
    current_mileage = db.Column(db.Integer, nullable=False)
    due_mileage = db.Column(db.Integer, nullable=False)
    
    # Cost
    estimated_cost = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float)
    
    # Assignment
    assigned_to = db.Column(db.String(200))
    assigned_technician = db.Column(db.String(100))
    
    # Additional info
    notes = db.Column(db.Text)
    parts_needed = db.Column(db.JSON)
    attachments = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'type': self.type,
            'description': self.description,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'priority': self.priority.value if isinstance(self.priority, Enum) else self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'current_mileage': self.current_mileage,
            'due_mileage': self.due_mileage,
            'estimated_cost': self.estimated_cost,
            'actual_cost': self.actual_cost,
            'assigned_to': self.assigned_to,
            'assigned_technician': self.assigned_technician,
            'notes': self.notes,
            'parts_needed': self.parts_needed,
            'attachments': self.attachments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MaintenanceItem {self.id}: {self.type} for {self.vehicle_id}>'

class Technician(db.Model):
    __tablename__ = 'technicians'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialization = db.Column(db.JSON) # List of strings
    status = db.Column(db.Enum(TechnicianStatus, name='technicianstatus', values_callable=lambda x: [e.value for e in x]), default=TechnicianStatus.AVAILABLE, nullable=False)
    rating = db.Column(db.Float, default=5.0)
    completed_jobs = db.Column(db.Integer, default=0)
    active_jobs = db.Column(db.Integer, default=0)
    certifications = db.Column(db.JSON) # List of strings
    hourly_rate = db.Column(db.Float, default=0.0)
    join_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialization': self.specialization,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'rating': self.rating,
            'completed_jobs': self.completed_jobs,
            'active_jobs': self.active_jobs,
            'certifications': self.certifications,
            'hourly_rate': self.hourly_rate,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Part(db.Model):
    __tablename__ = 'parts'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    min_quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_cost = db.Column(db.Float, default=0.0, nullable=False)
    supplier = db.Column(db.String(100))
    location = db.Column(db.String(100))
    last_restocked = db.Column(db.Date)
    used_in = db.Column(db.JSON) # List of strings (vehicle/maintenance types)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'part_number': self.part_number,
            'category': self.category,
            'quantity': self.quantity,
            'min_quantity': self.min_quantity,
            'unit_cost': self.unit_cost,
            'supplier': self.supplier,
            'location': self.location,
            'last_restocked': self.last_restocked.isoformat() if self.last_restocked else None,
            'used_in': self.used_in,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RecurringSchedule(db.Model):
    __tablename__ = 'recurring_schedules'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vehicle_id = db.Column(db.String(50), nullable=False)
    maintenance_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.Enum(FrequencyType, name='frequencytype', values_callable=lambda x: [e.value for e in x]), default=FrequencyType.MONTHLY, nullable=False)
    frequency_value = db.Column(db.Integer, default=1, nullable=False)
    estimated_cost = db.Column(db.Float, default=0.0)
    estimated_duration = db.Column(db.Float, default=0.0)
    assigned_to = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    last_executed = db.Column(db.DateTime)
    next_scheduled = db.Column(db.DateTime)
    total_executions = db.Column(db.Integer, default=0)
    created_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vehicle_id': self.vehicle_id,
            'maintenance_type': self.maintenance_type,
            'description': self.description,
            'frequency': self.frequency.value if isinstance(self.frequency, Enum) else self.frequency,
            'frequency_value': self.frequency_value,
            'estimated_cost': self.estimated_cost,
            'estimated_duration': self.estimated_duration,
            'assigned_to': self.assigned_to,
            'is_active': self.is_active,
            'last_executed': self.last_executed.isoformat() if self.last_executed else None,
            'next_scheduled': self.next_scheduled.isoformat() if self.next_scheduled else None,
            'total_executions': self.total_executions,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
