from app import db
from app.models.maintainance import MaintenanceItem, MaintenanceStatus, MaintenancePriority, Technician, TechnicianStatus, Part, RecurringSchedule, FrequencyType
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_

class MaintenanceService:
    
    @staticmethod
    def generate_id(prefix, model):
        """Generate unique ID with prefix"""
        last_item = model.query.order_by(model.id.desc()).first()
        new_num = 1
        
        if last_item and last_item.id.startswith(prefix):
            try:
                new_num = int(last_item.id[len(prefix):]) + 1
            except ValueError:
                pass
                
        return f'{prefix}{new_num:03d}'
    
    @staticmethod
    def generate_maintenance_id():
        return MaintenanceService.generate_id('M', MaintenanceItem)

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
        
        # Handle special fields
        if data.get('status'):
            item.status = MaintenanceStatus(data['status'])
            if data['status'] == 'completed' and not item.completed_date:
                item.completed_date = datetime.utcnow()
        
        if data.get('priority'):
            item.priority = MaintenancePriority(data['priority'])
        
        # Fields that can be updated dynamically
        # (field_name, require_not_none)
        updatable_fields = {
            'type': False, 'description': False, 'due_date': False, 
            'scheduled_date': False, 'completed_date': False, 
            'assigned_to': False, 'assigned_technician': False, 
            'notes': False, 'parts_needed': False, 'attachments': False,
            # Numeric fields originally checked for is not None
            'current_mileage': True, 'due_mileage': True, 
            'estimated_cost': True, 'actual_cost': True
        }
        
        for field, require_not_none in updatable_fields.items():
            if field in data:
                value = data[field]
                if require_not_none and value is None:
                    continue
                setattr(item, field, value)
        
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
    
    @staticmethod
    def get_cost_analytics():
        """Get detailed cost analytics"""
        # Total costs
        total_estimated = db.session.query(
            db.func.sum(MaintenanceItem.estimated_cost)
        ).scalar() or 0.0
        
        total_actual = db.session.query(
            db.func.sum(MaintenanceItem.actual_cost)
        ).filter(
            MaintenanceItem.actual_cost.isnot(None)
        ).scalar() or 0.0
        
        # Cost by vehicle
        by_vehicle = {}
        vehicles = db.session.query(MaintenanceItem.vehicle_id).distinct().all()
        
        for (vehicle_id,) in vehicles:
            vehicle_estimated = db.session.query(
                db.func.sum(MaintenanceItem.estimated_cost)
            ).filter(MaintenanceItem.vehicle_id == vehicle_id).scalar() or 0.0
            
            vehicle_actual = db.session.query(
                db.func.sum(MaintenanceItem.actual_cost)
            ).filter(
                MaintenanceItem.vehicle_id == vehicle_id,
                MaintenanceItem.actual_cost.isnot(None)
            ).scalar() or 0.0
            
            by_vehicle[vehicle_id] = {
                'estimated': float(vehicle_estimated),
                'actual': float(vehicle_actual),
                'variance': float(vehicle_actual - vehicle_estimated)
            }
        
        # Cost by maintenance type
        by_type = {}
        types = db.session.query(MaintenanceItem.type).distinct().all()
        
        for (maint_type,) in types:
            type_estimated = db.session.query(
                db.func.sum(MaintenanceItem.estimated_cost)
            ).filter(MaintenanceItem.type == maint_type).scalar() or 0.0
            
            type_actual = db.session.query(
                db.func.sum(MaintenanceItem.actual_cost)
            ).filter(
                MaintenanceItem.type == maint_type,
                MaintenanceItem.actual_cost.isnot(None)
            ).scalar() or 0.0
            
            by_type[maint_type] = {
                'estimated': float(type_estimated),
                'actual': float(type_actual),
                'count': MaintenanceItem.query.filter(MaintenanceItem.type == maint_type).count()
            }
        
        variance = total_actual - total_estimated
        variance_percent = (variance / total_estimated * 100) if total_estimated > 0 else 0
        
        return {
            'total_estimated': float(total_estimated),
            'total_actual': float(total_actual),
            'variance': float(variance),
            'variance_percent': float(variance_percent),
            'by_vehicle': by_vehicle,
            'by_type': by_type,
            'completed_count': MaintenanceItem.query.filter(
                MaintenanceItem.status == MaintenanceStatus.COMPLETED
            ).count(),
            'pending_count': MaintenanceItem.query.filter(
                MaintenanceItem.status.in_([
                    MaintenanceStatus.SCHEDULED,
                    MaintenanceStatus.DUE_SOON,
                    MaintenanceStatus.OVERDUE,
                    MaintenanceStatus.IN_PROGRESS
                ])
            ).count()
        }
    
    @staticmethod
    def get_maintenance_trends(period='month', limit=12):
        """Get maintenance trends over time"""
        all_items = MaintenanceItem.query.all()
        
        trends = {
            'periods': [],
            'total_items': [],
            'completed': [],
            'estimated_cost': [],
            'actual_cost': [],
        }
        
        # Generate period labels
        today = date.today()
        for i in range(limit - 1, -1, -1):
            if period == 'week':
                period_start = today - timedelta(weeks=i)
                period_label = period_start.strftime('%Y-W%W')
            elif period == 'quarter':
                months_back = i * 3
                period_start = today - timedelta(days=months_back * 30)
                period_label = f'{period_start.year}-Q{(period_start.month - 1) // 3 + 1}'
            elif period == 'year':
                period_start = date(today.year - i, 1, 1)
                period_label = str(period_start.year)
            else:  # month (default)
                months_back = i
                year = today.year - (today.month - 1 - months_back) // 12
                month = ((today.month - 1 - months_back) % 12) + 1
                period_start = date(year, month, 1)
                period_label = period_start.strftime('%Y-%m')
            
            trends['periods'].append(period_label)
            
            # Count items for this period
            # Note: This is a simplified filtering, in production use DB queries
            period_items = [item for item in all_items if item.created_at and 
                          item.created_at.strftime('%Y-%m') == period_start.strftime('%Y-%m')] # Rough approx
            
            trends['total_items'].append(len(period_items))
            trends['completed'].append(
                len([i for i in period_items if i.status == MaintenanceStatus.COMPLETED])
            )
            
            est_cost = sum(i.estimated_cost or 0 for i in period_items)
            act_cost = sum(i.actual_cost or 0 for i in period_items if i.actual_cost)
            
            trends['estimated_cost'].append(float(est_cost))
            trends['actual_cost'].append(float(act_cost))
        
        return trends
    
    @staticmethod
    def get_overdue_items():
        """Get all overdue maintenance items"""
        items = MaintenanceItem.query.filter(
            MaintenanceItem.status == MaintenanceStatus.OVERDUE
        ).order_by(MaintenanceItem.due_date.asc()).all()
        
        return [item.to_dict() for item in items]
    
    @staticmethod
    def get_upcoming_items(days=30):
        """Get upcoming maintenance items"""
        future_date = date.today() + timedelta(days=days)
        
        items = MaintenanceItem.query.filter(
            MaintenanceItem.status.in_([
                MaintenanceStatus.SCHEDULED,
                MaintenanceStatus.DUE_SOON
            ]),
            MaintenanceItem.due_date <= future_date
        ).order_by(MaintenanceItem.due_date.asc()).all()
        
        return [item.to_dict() for item in items]
    
    @staticmethod
    def search_maintenance(query, page=1, per_page=10):
        """Search maintenance items by query string"""
        search_query = MaintenanceItem.query.filter(
            or_(
                MaintenanceItem.type.ilike(f'%{query}%'),
                MaintenanceItem.description.ilike(f'%{query}%'),
                MaintenanceItem.vehicle_id.ilike(f'%{query}%'),
                MaintenanceItem.id.ilike(f'%{query}%'),
                MaintenanceItem.assigned_to.ilike(f'%{query}%'),
                MaintenanceItem.assigned_technician.ilike(f'%{query}%')
            )
        ).order_by(MaintenanceItem.due_date.desc())
        
        pagination = search_query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'page': page,
            'per_page': per_page
        }

    # ==================== Technician Methods ====================
    @staticmethod
    def get_all_technicians():
        """Get all technicians"""
        technicians = Technician.query.all()
        return [t.to_dict() for t in technicians]

    @staticmethod
    def create_technician(data):
        """Create a new technician"""
        technician = Technician(
            id=MaintenanceService.generate_id('T', Technician),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            specialization=data.get('specialization', []),
            status=TechnicianStatus(data.get('status', 'available')),
            certifications=data.get('certifications', []),
            hourly_rate=data.get('hourly_rate', 0.0),
            join_date=data.get('join_date', date.today())
        )
        db.session.add(technician)
        db.session.commit()
        return technician

    @staticmethod
    def update_technician(tech_id, data):
        """Update a technician"""
        tech = Technician.query.get(tech_id)
        if not tech:
            return None
        
        for key, value in data.items():
            if hasattr(tech, key):
                if key == 'status':
                    setattr(tech, key, TechnicianStatus(value))
                else:
                    setattr(tech, key, value)
        
        tech.updated_at = datetime.utcnow()
        db.session.commit()
        return tech

    @staticmethod
    def delete_technician(tech_id):
        """Delete a technician"""
        tech = Technician.query.get(tech_id)
        if not tech:
            return False
        db.session.delete(tech)
        db.session.commit()
        return True

    # ==================== Part Methods ====================
    @staticmethod
    def get_all_parts(search_query=None):
        """Get all parts, optionally filtered by search query"""
        query = Part.query
        if search_query:
            query = query.filter(
                or_(
                    Part.name.ilike(f'%{search_query}%'),
                    Part.part_number.ilike(f'%{search_query}%'),
                    Part.category.ilike(f'%{search_query}%')
                )
            )
        parts = query.all()
        return [p.to_dict() for p in parts]

    @staticmethod
    def create_part(data):
        """Create a new part"""
        part = Part(
            id=MaintenanceService.generate_id('P', Part),
            name=data['name'],
            part_number=data['part_number'],
            category=data['category'],
            quantity=data['quantity'],
            min_quantity=data['min_quantity'],
            unit_cost=data['unit_cost'],
            supplier=data.get('supplier'),
            location=data.get('location'),
            used_in=data.get('used_in', []),
            last_restocked=date.today() if data.get('quantity', 0) > 0 else None
        )
        db.session.add(part)
        db.session.commit()
        return part

    @staticmethod
    def update_part(part_id, data):
        """Update a part"""
        part = Part.query.get(part_id)
        if not part:
            return None
        
        # Check if restocking happened
        if 'quantity' in data and data['quantity'] > part.quantity:
            part.last_restocked = date.today()

        for key, value in data.items():
            if hasattr(part, key):
                setattr(part, key, value)
        
        part.updated_at = datetime.utcnow()
        db.session.commit()
        return part

    @staticmethod
    def delete_part(part_id):
        """Delete a part"""
        part = Part.query.get(part_id)
        if not part:
            return False
        db.session.delete(part)
        db.session.commit()
        return True

    # ==================== Recurring Schedule Methods ====================
    @staticmethod
    def get_all_recurring_schedules():
        """Get all recurring schedules"""
        schedules = RecurringSchedule.query.all()
        return [s.to_dict() for s in schedules]

    @staticmethod
    def create_recurring_schedule(data):
        """Create a new recurring schedule"""
        # Calculate next scheduled date
        now = datetime.utcnow()
        freq_type = data['frequency']
        freq_val = data['frequency_value']
        next_date = now
        
        if freq_type == 'daily':
            next_date = now + timedelta(days=freq_val)
        elif freq_type == 'weekly':
            next_date = now + timedelta(weeks=freq_val)
        elif freq_type == 'monthly':
            # Simplified monthly addition
            next_month = now.month + freq_val
            year_add = (next_month - 1) // 12
            new_month = ((next_month - 1) % 12) + 1
            next_date = now.replace(year=now.year + year_add, month=new_month)
        elif freq_type == 'quarterly':
             # Simplified quarterly addition
            next_month = now.month + (freq_val * 3)
            year_add = (next_month - 1) // 12
            new_month = ((next_month - 1) % 12) + 1
            next_date = now.replace(year=now.year + year_add, month=new_month)
        elif freq_type == 'yearly':
            next_date = now.replace(year=now.year + freq_val)
        elif freq_type == 'mileage-based':
            # Default to 30 days for mileage based initial schedule estimate
            next_date = now + timedelta(days=30)

        schedule = RecurringSchedule(
            id=MaintenanceService.generate_id('RS', RecurringSchedule),
            name=data['name'],
            vehicle_id=data['vehicle_id'],
            maintenance_type=data['maintenance_type'],
            description=data.get('description'),
            frequency=FrequencyType(data['frequency']),
            frequency_value=data['frequency_value'],
            estimated_cost=data.get('estimated_cost', 0.0),
            estimated_duration=data.get('estimated_duration', 0.0),
            assigned_to=data.get('assigned_to'),
            is_active=data.get('is_active', True),
            next_scheduled=next_date
        )
        db.session.add(schedule)
        db.session.commit()
        return schedule

    @staticmethod
    def update_recurring_schedule(schedule_id, data):
        """Update a recurring schedule"""
        schedule = RecurringSchedule.query.get(schedule_id)
        if not schedule:
            return None
        
        for key, value in data.items():
            if hasattr(schedule, key):
                if key == 'frequency':
                    setattr(schedule, key, FrequencyType(value))
                else:
                    setattr(schedule, key, value)
        
        schedule.updated_at = datetime.utcnow()
        db.session.commit()
        return schedule

    @staticmethod
    def delete_recurring_schedule(schedule_id):
        """Delete a recurring schedule"""
        schedule = RecurringSchedule.query.get(schedule_id)
        if not schedule:
            return False
        db.session.delete(schedule)
        db.session.commit()
        return True
