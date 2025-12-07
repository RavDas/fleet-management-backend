from flask import Blueprint, request, jsonify
from models.maintenance import Maintenance
from app import db
import requests
from config import Config

bp = Blueprint('maintenance', __name__, url_prefix='/api/maintenance')

@bp.route('/', methods=['POST'])
def create_maintenance():
    data = request.get_json()
    
    # Removing east west traffic.
    #
    # # Verify vehicle exists in vehicle service
    # # vehicle_response = requests.get(f"{Config.VEHICLE_SERVICE_URL}/api/vehicles/{data['vehicle_id']}")
    # # if vehicle_response.status_code != 200:
    # #     return jsonify({'error': 'Vehicle not found'}), 404

    maintenance = Maintenance(
        vehicle_id=data['vehicle_id'],
        maintenance_type=data['maintenance_type'],
        description=data.get('description'),
        scheduled_date=data['scheduled_date'],
        status='SCHEDULED',
        cost=data.get('cost')
    )
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({'id': maintenance.id}), 201

@bp.route('/', methods=['GET'])
def get_all_maintenance():
    maintenance_records = Maintenance.query.all()
    return jsonify([{
        'id': m.id,
        'vehicle_id': m.vehicle_id,
        'maintenance_type': m.maintenance_type,
        'status': m.status,
        'scheduled_date': m.scheduled_date,
        'completed_date': m.completed_date
    } for m in maintenance_records])

@bp.route('/<int:id>', methods=['GET'])
def get_maintenance(id):
    maintenance = Maintenance.query.get_or_404(id)
    return jsonify({
        'id': maintenance.id,
        'vehicle_id': maintenance.vehicle_id,
        'maintenance_type': maintenance.maintenance_type,
        'description': maintenance.description,
        'status': maintenance.status,
        'scheduled_date': maintenance.scheduled_date,
        'completed_date': maintenance.completed_date,
        'cost': maintenance.cost
    })

@bp.route('/<int:id>/complete', methods=['PUT'])
def complete_maintenance(id):
    maintenance = Maintenance.query.get_or_404(id)
    maintenance.status = 'COMPLETED'
    maintenance.completed_date = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Maintenance marked as completed'})