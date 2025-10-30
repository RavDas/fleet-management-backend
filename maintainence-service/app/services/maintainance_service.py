from app import db
from app.models.maintainance import MaintenanceItem, MaintenanceStatus, MaintenancePriority
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_

class MaintenanceService:
    
    @staticmethod
    def generate_maintenance_id():
        """Generate unique maintenance ID"""
        last_item = MaintenanceItem.query.order_by(MaintenanceItem.id.desc()).first()
        if last_item:
            last_num = int(last_item.id.split('-')[1])
            new_num = last_num + 1
        else:
            new_num = 1
        return f'M{new_num:03d}'
    
    @staticmethod
    def create_maintenance_item(data):
        """Create a new maintenance item"""
        maintenance_id = MaintenanceService.generate_maintenance_id()
        
        maintenance_item = MaintenanceItem(
            id=maintenance_id,
            vehicle_id=data['vehicle'],
            type=data['type'],
            description=data.get('description'),
            priority=MaintenancePriority(data['priority']),
            due_date=data['dueDate'],
            current_mileage=data['currentMileage'],
            due_mileage=data['dueMileage'],
            estimated_cost=data.get('cost', 0.0),
            assigned_to=data.get('assignedTo'),
            notes=data.get('notes'),
            parts_needed=data.get('partsNeeded'),
            status=MaintenanceService._determine_status(data['dueDate'], data['currentMileage'], data['dueMileage'])
        )
        
        db.session.add(maintenance_item)
        db.session.commit()
        return maintenance_item
    
    @staticmethod
    def _determine_status(due_date, current_mileage, due_mileage):
        """Automatically determine maintenance status"""
        today = date.today()
        days_until_due = (due_date - today).days
        mileage_diff = due_mileage - current_mileage
        
        # Overdue if past due date or past due mileage
        if days_until_due < 0 or current_mileage >= due_mileage:
            return MaintenanceStatus.OVERDUE
        
        # Due soon if within 7 days or within 500 km
        if days_until_due <= 7 or mileage_diff <= 500:
            return MaintenanceStatus.DUE_SOON
        
        return MaintenanceStatus.SCHEDULED
    
    @staticmethod
    def get_all_maintenance_items(filters=None, page=1, per_page=10):
        """Get all maintenance items with optional filtering and pagination"""
        query = MaintenanceItem.query
        
        if filters:
            if 'vehicle' in filters:
                query = query.filter(MaintenanceItem.vehicle_id == filters['vehicle'])
            
            if 'status' in filters:
                statuses = filters['status'] if isinstance(filters['status'], list) else [filters['status']]
                query = query.filter(MaintenanceItem.status.in_(statuses))
            
            if 'priority' in filters:
                priorities = filters['priority'] if isinstance(filters['priority'], list) else [filters['priority']]
                query = query.filter(MaintenanceItem.priority.in_(priorities))
            
            if 'assignedTo' in filters:
                query = query.filter(MaintenanceItem.assigned_to == filters['assignedTo'])
            
            if 'dueDateFrom' in filters:
                query = query.filter(MaintenanceItem.due_date >= filters['dueDateFrom'])
            
            if 'dueDateTo' in filters:
                query = query.filter(MaintenanceItem.due_date <= filters['dueDateTo'])
        
        # Order by priority and due date
        query = query.order_by(
            MaintenanceItem.status.desc(),
            MaintenanceItem.priority.desc(),
            MaintenanceItem.due_date.asc()
        )
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        }
    
    @staticmethod
    def get_maintenance_item(item_id):
        """Get a single maintenance item by ID"""
        return MaintenanceItem.query.get(item_id)
    
    @staticmethod
    def update_maintenance_item(item_id, data):
        """Update a maintenance item"""
        item = MaintenanceItem.query.get(item_id)
        if not item:
            return None
        
        # Update fields
        for key, value in data.items():
            if key == 'status' and value:
                item.status = MaintenanceStatus(value)
                if value == 'completed':
                    item.completed_date = datetime.utcnow()
            elif key == 'priority' and value:
                item.priority = MaintenancePriority(value)
            elif key == 'dueDate' and value:
                item.due_date = value
            elif key == 'scheduledDate' and value:
                item.scheduled_date = value
            elif key == 'currentMileage' and value is not None:
                item.current_mileage = value
            elif key == 'dueMileage' and value is not None:
                item.due_mileage = value
            elif key == 'cost' and value is not None:
                item.estimated_cost = value
            elif key == 'actualCost' and value is not None:
                item.actual_cost = value
            elif hasattr(item, key) and key not in ['id', 'vehicle', 'createdAt', 'updatedAt']:
                setattr(item, key if key != 'assignedTo' else 'assigned_to', value)
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        return item
    
    @staticmethod
    def delete_maintenance_item(item_id):
        """Delete a maintenance item"""
        item = MaintenanceItem.query.get(item_id)
        if not item:
            return False
        
        db.session.delete(item)
        db.session.commit()
        return True
    
    @staticmethod
    def get_maintenance_summary():
        """Get summary statistics for maintenance items"""
        total = MaintenanceItem.query.count()
        
        overdue = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.OVERDUE
        ).count()
        
        due_soon = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.DUE_SOON
        ).count()
        
        in_progress = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.IN_PROGRESS
        ).count()
        
        completed_this_month = MaintenanceItem.query.filter(
            and_(
                MaintenanceItem.status == MaintenanceStatus.COMPLETED,
                MaintenanceItem.completed_date >= datetime.utcnow().replace(day=1)
            )
        ).count()
        
        scheduled_cost = db.session.query(
            db.func.sum(MaintenanceItem.estimated_cost)
        ).filter(
            MaintenanceItem.status.in_([MaintenanceStatus.SCHEDULED, MaintenanceStatus.IN_PROGRESS])
        ).scalar() or 0
        
        return {
            'total': total,
            'overdue': overdue,
            'dueSoon': due_soon,
            'upcoming': overdue + due_soon,
            'inProgress': in_progress,
            'completedThisMonth': completed_this_month,
            'scheduledCost': float(scheduled_cost)
        }
    
    @staticmethod
    def get_vehicle_maintenance_history(vehicle_id):
        """Get maintenance history for a specific vehicle"""
        items = MaintenanceItem.query.filter(
            MaintenanceItem.vehicle_id == vehicle_id
        ).order_by(MaintenanceItem.due_date.desc()).all()
        
        return [item.to_dict() for item in items]
    
    @staticmethod
    def update_maintenance_status_bulk():
        """Background job to update maintenance statuses based on current date and mileage"""
        items = MaintenanceItem.query.filter(
            MaintenanceItem.status.in_([MaintenanceStatus.SCHEDULED, MaintenanceStatus.DUE_SOON])
        ).all()
        
        updated_count = 0
        for item in items:
            new_status = MaintenanceService._determine_status(
                item.due_date,
                item.current_mileage,
                item.due_mileage
            )
            if item.status != new_status:
                item.status = new_status
                item.updated_at = datetime.utcnow()
                updated_count += 1
        
        db.session.commit()
        return updated_count