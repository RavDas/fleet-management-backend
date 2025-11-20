"""
Flask-RESTX API Routes with Swagger Documentation
Provides OpenAPI/Swagger UI for the Maintenance Service
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.maintainance_service import MaintenanceService
from app.schemas.maintainance_schema import (
    MaintenanceItemCreateSchema,
    MaintenanceItemUpdateSchema
)
from marshmallow import ValidationError

# Create API namespace
api = Namespace('maintenance', description='Maintenance management operations')

# ==================== Swagger Models ====================

# Maintenance Item Model (for responses)
maintenance_item_model = api.model('MaintenanceItem', {
    'id': fields.String(required=True, description='Maintenance item ID', example='M001'),
    'vehicle_id': fields.String(required=True, description='Vehicle ID', example='VH-001'),
    'type': fields.String(required=True, description='Maintenance type', example='Oil Change'),
    'description': fields.String(description='Detailed description', example='Regular oil and filter change'),
    'status': fields.String(required=True, description='Current status', 
                           enum=['overdue', 'due_soon', 'scheduled', 'in_progress', 'completed', 'cancelled'],
                           example='scheduled'),
    'priority': fields.String(required=True, description='Priority level',
                             enum=['low', 'medium', 'high', 'critical'],
                             example='medium'),
    'due_date': fields.Date(required=True, description='Due date', example='2024-12-31'),
    'scheduled_date': fields.DateTime(description='Scheduled date and time'),
    'completed_date': fields.DateTime(description='Completion date and time'),
    'current_mileage': fields.Integer(required=True, description='Current vehicle mileage', example=45000),
    'due_mileage': fields.Integer(required=True, description='Mileage when maintenance is due', example=50000),
    'estimated_cost': fields.Float(description='Estimated cost', example=150.50),
    'actual_cost': fields.Float(description='Actual cost after completion', example=175.00),
    'assigned_to': fields.String(description='Service center or technician', example='Service Center A'),
    'assigned_technician': fields.String(description='Assigned technician name'),
    'notes': fields.String(description='Additional notes'),
    'parts_needed': fields.Raw(description='JSON list of required parts'),
    'attachments': fields.Raw(description='JSON list of attachment URLs'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
})

# Create Model (for POST requests)
maintenance_create_model = api.model('MaintenanceCreate', {
    'id': fields.String(required=True, description='Unique maintenance item ID', example='M006'),
    'vehicle_id': fields.String(required=True, description='Vehicle ID', example='VH-001'),
    'type': fields.String(required=True, description='Maintenance type', example='Oil Change'),
    'description': fields.String(description='Detailed description'),
    'status': fields.String(description='Initial status', example='scheduled'),
    'priority': fields.String(description='Priority level', example='medium'),
    'due_date': fields.Date(required=True, description='Due date', example='2024-12-31'),
    'current_mileage': fields.Integer(required=True, description='Current mileage', example=45000),
    'due_mileage': fields.Integer(required=True, description='Mileage when due', example=50000),
    'estimated_cost': fields.Float(description='Estimated cost', example=150.50),
    'assigned_to': fields.String(description='Service center', example='Service Center A'),
    'assigned_technician': fields.String(description='Technician name'),
    'notes': fields.String(description='Additional notes'),
})

# Update Model (for PUT/PATCH requests)
maintenance_update_model = api.model('MaintenanceUpdate', {
    'type': fields.String(description='Maintenance type'),
    'description': fields.String(description='Detailed description'),
    'status': fields.String(description='Status'),
    'priority': fields.String(description='Priority level'),
    'due_date': fields.Date(description='Due date'),
    'scheduled_date': fields.DateTime(description='Scheduled date'),
    'completed_date': fields.DateTime(description='Completion date'),
    'current_mileage': fields.Integer(description='Current mileage'),
    'due_mileage': fields.Integer(description='Mileage when due'),
    'estimated_cost': fields.Float(description='Estimated cost'),
    'actual_cost': fields.Float(description='Actual cost'),
    'assigned_to': fields.String(description='Service center'),
    'assigned_technician': fields.String(description='Technician name'),
    'notes': fields.String(description='Additional notes'),
    'parts_needed': fields.Raw(description='Required parts'),
    'attachments': fields.Raw(description='Attachments'),
})

# Pagination Model
pagination_model = api.model('PaginatedMaintenanceItems', {
    'items': fields.List(fields.Nested(maintenance_item_model), description='List of maintenance items'),
    'total': fields.Integer(description='Total number of items'),
    'page': fields.Integer(description='Current page number'),
    'per_page': fields.Integer(description='Items per page'),
    'pages': fields.Integer(description='Total number of pages'),
})

# Summary Model
summary_model = api.model('MaintenanceSummary', {
    'total_items': fields.Integer(description='Total maintenance items'),
    'by_status': fields.Raw(description='Count by status'),
    'by_priority': fields.Raw(description='Count by priority'),
    'total_estimated_cost': fields.Float(description='Total estimated costs'),
    'total_actual_cost': fields.Float(description='Total actual costs'),
    'overdue_count': fields.Integer(description='Number of overdue items'),
    'due_soon_count': fields.Integer(description='Number of items due soon'),
})

# Error Model
error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'errors': fields.Raw(description='Validation errors'),
})

# ==================== API Resources ====================

@api.route('/')
class MaintenanceList(Resource):
    @api.doc('list_maintenance_items',
             params={
                 'page': 'Page number (default: 1)',
                 'per_page': 'Items per page (default: 10)',
                 'vehicle': 'Filter by vehicle ID',
                 'status': 'Filter by status (can specify multiple)',
                 'priority': 'Filter by priority (can specify multiple)',
                 'assignedTo': 'Filter by assignment'
             })
    @api.marshal_with(pagination_model, code=200, description='Success')
    @api.response(500, 'Internal Server Error', error_model)
    def get(self):
        """List all maintenance items with optional filtering and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            filters = {}
            if request.args.get('vehicle'):
                filters['vehicle'] = request.args.get('vehicle')
            if request.args.get('status'):
                filters['status'] = request.args.getlist('status')
            if request.args.get('priority'):
                filters['priority'] = request.args.getlist('priority')
            if request.args.get('assignedTo'):
                filters['assignedTo'] = request.args.get('assignedTo')
            
            result = MaintenanceService.get_all_maintenance_items(filters, page, per_page)
            return result, 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
    
    @api.doc('create_maintenance_item')
    @api.expect(maintenance_create_model, validate=True)
    @api.marshal_with(maintenance_item_model, code=201, description='Created')
    @api.response(400, 'Validation Error', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def post(self):
        """Create a new maintenance item"""
        try:
            schema = MaintenanceItemCreateSchema()
            data = schema.load(request.json)
            
            item = MaintenanceService.create_maintenance_item(data)
            return item.to_dict(), 201
        
        except ValidationError as e:
            api.abort(400, f'Validation error', errors=e.messages)
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/<string:item_id>')
@api.param('item_id', 'The maintenance item identifier')
class MaintenanceItem(Resource):
    @api.doc('get_maintenance_item')
    @api.marshal_with(maintenance_item_model, code=200, description='Success')
    @api.response(404, 'Maintenance item not found', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def get(self, item_id):
        """Get a specific maintenance item by ID"""
        try:
            item = MaintenanceService.get_maintenance_item(item_id)
            if not item:
                api.abort(404, f'Maintenance item {item_id} not found')
            
            return item.to_dict(), 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
    
    @api.doc('update_maintenance_item')
    @api.expect(maintenance_update_model, validate=True)
    @api.marshal_with(maintenance_item_model, code=200, description='Success')
    @api.response(400, 'Validation Error', error_model)
    @api.response(404, 'Maintenance item not found', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def put(self, item_id):
        """Update a maintenance item (full update)"""
        try:
            schema = MaintenanceItemUpdateSchema()
            data = schema.load(request.json, partial=False)
            
            item = MaintenanceService.update_maintenance_item(item_id, data)
            if not item:
                api.abort(404, f'Maintenance item {item_id} not found')
            
            return item.to_dict(), 200
        
        except ValidationError as e:
            api.abort(400, f'Validation error', errors=e.messages)
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
    
    @api.doc('partial_update_maintenance_item')
    @api.expect(maintenance_update_model, validate=True)
    @api.marshal_with(maintenance_item_model, code=200, description='Success')
    @api.response(400, 'Validation Error', error_model)
    @api.response(404, 'Maintenance item not found', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def patch(self, item_id):
        """Partially update a maintenance item"""
        try:
            schema = MaintenanceItemUpdateSchema()
            data = schema.load(request.json, partial=True)
            
            item = MaintenanceService.update_maintenance_item(item_id, data)
            if not item:
                api.abort(404, f'Maintenance item {item_id} not found')
            
            return item.to_dict(), 200
        
        except ValidationError as e:
            api.abort(400, f'Validation error', errors=e.messages)
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')
    
    @api.doc('delete_maintenance_item')
    @api.response(200, 'Success')
    @api.response(404, 'Maintenance item not found', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def delete(self, item_id):
        """Delete a maintenance item"""
        try:
            success = MaintenanceService.delete_maintenance_item(item_id)
            if not success:
                api.abort(404, f'Maintenance item {item_id} not found')
            
            return {'message': 'Maintenance item deleted successfully'}, 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/summary')
class MaintenanceSummary(Resource):
    @api.doc('get_maintenance_summary')
    @api.marshal_with(summary_model, code=200, description='Success')
    @api.response(500, 'Internal Server Error', error_model)
    def get(self):
        """Get maintenance summary statistics"""
        try:
            summary = MaintenanceService.get_maintenance_summary()
            return summary, 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/vehicle/<string:vehicle_id>/history')
@api.param('vehicle_id', 'The vehicle identifier')
class VehicleHistory(Resource):
    @api.doc('get_vehicle_maintenance_history')
    @api.marshal_list_with(maintenance_item_model, code=200, description='Success')
    @api.response(500, 'Internal Server Error', error_model)
    def get(self, vehicle_id):
        """Get maintenance history for a specific vehicle"""
        try:
            history = MaintenanceService.get_vehicle_maintenance_history(vehicle_id)
            return history, 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')


@api.route('/status/update-bulk')
class BulkStatusUpdate(Resource):
    @api.doc('update_statuses_bulk')
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error', error_model)
    def post(self):
        """Background job endpoint to update maintenance statuses based on due dates"""
        try:
            updated = MaintenanceService.update_maintenance_status_bulk()
            return {
                'message': f'Updated {updated} maintenance items',
                'updated_count': updated
            }, 200
        
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

