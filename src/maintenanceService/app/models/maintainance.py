from app import db
from datetime import datetime
from enum import Enum

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

class MaintenanceItem(db.Model):
    __tablename__ = 'maintenance_items'
    
    id = db.Column(db.String(50), primary_key=True)
    vehicle_id = db.Column(db.String(50), nullable=False, index=True)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(MaintenanceStatus), default=MaintenanceStatus.SCHEDULED, nullable=False)
    priority = db.Column(db.Enum(MaintenancePriority), default=MaintenancePriority.MEDIUM, nullable=False)
    
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
            'vehicle': self.vehicle_id,
            'type': self.type,
            'description': self.description,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'priority': self.priority.value if isinstance(self.priority, Enum) else self.priority,
            'dueDate': self.due_date.isoformat() if self.due_date else None,
            'scheduledDate': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completedDate': self.completed_date.isoformat() if self.completed_date else None,
            'currentMileage': self.current_mileage,
            'dueMileage': self.due_mileage,
            'cost': self.estimated_cost,
            'actualCost': self.actual_cost,
            'assignedTo': self.assigned_to,
            'assignedTechnician': self.assigned_technician,
            'notes': self.notes,
            'partsNeeded': self.parts_needed,
            'attachments': self.attachments,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<MaintenanceItem {self.id}: {self.type} for {self.vehicle_id}>'
