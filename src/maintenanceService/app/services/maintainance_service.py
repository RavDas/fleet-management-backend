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
            # Try to extract number from ID (M001, M002, etc.)
            try:
                if last_item.id.startswith('M'):
                    last_num = int(last_item.id[1:])
                    new_num = last_num + 1
                else:
                    new_num = 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1
        return f'M{new_num:03d}'
    
    @staticmethod
    def create_maintenance_item(data):
        """Create a new maintenance item"""
        # Use provided ID or generate one
        maintenance_id = data.get('id') or MaintenanceService.generate_maintenance_id()
        
        # Determine status if not provided
        status = data.get('status')
        if not status:
            status = MaintenanceService._determine_status(
                data['due_date'], 
                data['current_mileage'], 
                data['due_mileage']
            ).value
        
        maintenance_item = MaintenanceItem(
            id=maintenance_id,
            vehicle_id=data['vehicle_id'],
            type=data['type'],
            description=data.get('description'),
            priority=MaintenancePriority(data['priority']),
            status=MaintenanceStatus(status),
            due_date=data['due_date'],
            current_mileage=data['current_mileage'],
            due_mileage=data['due_mileage'],
            estimated_cost=data.get('estimated_cost', 0.0),
            assigned_to=data.get('assigned_to'),
            assigned_technician=data.get('assigned_technician'),
            notes=data.get('notes'),
            parts_needed=data.get('parts_needed')
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
            'page': page,
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
        
        # Update fields with snake_case
        if 'status' in data and data['status']:
            item.status = MaintenanceStatus(data['status'])
            if data['status'] == 'completed' and not item.completed_date:
                item.completed_date = datetime.utcnow()
        
        if 'priority' in data and data['priority']:
            item.priority = MaintenancePriority(data['priority'])
        
        if 'type' in data:
            item.type = data['type']
        
        if 'description' in data:
            item.description = data['description']
        
        if 'due_date' in data:
            item.due_date = data['due_date']
        
        if 'scheduled_date' in data:
            item.scheduled_date = data['scheduled_date']
        
        if 'completed_date' in data:
            item.completed_date = data['completed_date']
        
        if 'current_mileage' in data and data['current_mileage'] is not None:
            item.current_mileage = data['current_mileage']
        
        if 'due_mileage' in data and data['due_mileage'] is not None:
            item.due_mileage = data['due_mileage']
        
        if 'estimated_cost' in data and data['estimated_cost'] is not None:
            item.estimated_cost = data['estimated_cost']
        
        if 'actual_cost' in data and data['actual_cost'] is not None:
            item.actual_cost = data['actual_cost']
        
        if 'assigned_to' in data:
            item.assigned_to = data['assigned_to']
        
        if 'assigned_technician' in data:
            item.assigned_technician = data['assigned_technician']
        
        if 'notes' in data:
            item.notes = data['notes']
        
        if 'parts_needed' in data:
            item.parts_needed = data['parts_needed']
        
        if 'attachments' in data:
            item.attachments = data['attachments']
        
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
        
        # Count by status
        by_status = {}
        for status in MaintenanceStatus:
            count = MaintenanceItem.query.filter(MaintenanceItem.status == status).count()
            by_status[status.value] = count
        
        # Count by priority
        by_priority = {}
        for priority in MaintenancePriority:
            count = MaintenanceItem.query.filter(MaintenanceItem.priority == priority).count()
            by_priority[priority.value] = count
        
        overdue_count = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.OVERDUE
        ).count()
        
        due_soon_count = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.DUE_SOON
        ).count()
        
        # Calculate total estimated cost for active maintenance
        total_estimated_cost = db.session.query(
            db.func.sum(MaintenanceItem.estimated_cost)
        ).filter(
            MaintenanceItem.status.in_([
                MaintenanceStatus.SCHEDULED, 
                MaintenanceStatus.IN_PROGRESS,
                MaintenanceStatus.DUE_SOON,
                MaintenanceStatus.OVERDUE
            ])
        ).scalar() or 0.0
        
        # Calculate total actual cost for completed maintenance
        total_actual_cost = db.session.query(
            db.func.sum(MaintenanceItem.actual_cost)
        ).filter(
            MaintenanceItem.status == MaintenanceStatus.COMPLETED
        ).scalar() or 0.0
        
        return {
            'total_items': total,
            'by_status': by_status,
            'by_priority': by_priority,
            'total_estimated_cost': float(total_estimated_cost),
            'total_actual_cost': float(total_actual_cost),
            'overdue_count': overdue_count,
            'due_soon_count': due_soon_count
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
        return updated_count