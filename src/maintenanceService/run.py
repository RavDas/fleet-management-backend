from app import create_app, db
from app.models.maintainance import MaintenanceItem
import os

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make shell context for flask shell command"""
    return {
        'db': db,
        'MaintenanceItem': MaintenanceItem
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    from datetime import date, timedelta
    
    # Check if data already exists
    if MaintenanceItem.query.first():
        print("Database already has data. Skipping seed.")
        return
    
    sample_data = [
        {
            'id': 'M001',
            'vehicle_id': 'VH-0123',
            'type': 'Oil Change',
            'status': 'overdue',
            'priority': 'high',
            'due_date': date.today() - timedelta(days=8),
            'current_mileage': 45230,
            'due_mileage': 45000,
            'estimated_cost': 150.0,
            'assigned_to': 'Service Center A'
        },
        {
            'id': 'M002',
            'vehicle_id': 'VH-0456',
            'type': 'Brake Inspection',
            'status': 'in_progress',
            'priority': 'medium',
            'due_date': date.today() + timedelta(days=3),
            'current_mileage': 67890,
            'due_mileage': 68000,
            'estimated_cost': 300.0,
            'assigned_to': 'Service Center B'
        },
        {
            'id': 'M003',
            'vehicle_id': 'VH-0789',
            'type': 'Tire Rotation',
            'status': 'scheduled',
            'priority': 'low',
            'due_date': date.today() + timedelta(days=10),
            'current_mileage': 23456,
            'due_mileage': 25000,
            'estimated_cost': 80.0,
            'assigned_to': 'Service Center A'
        },
        {
            'id': 'M004',
            'vehicle_id': 'VH-0321',
            'type': 'Annual Inspection',
            'status': 'due_soon',
            'priority': 'high',
            'due_date': date.today() + timedelta(days=2),
            'current_mileage': 89123,
            'due_mileage': 90000,
            'estimated_cost': 500.0,
            'assigned_to': 'Service Center C'
        },
        {
            'id': 'M005',
            'vehicle_id': 'VH-0567',
            'type': 'Engine Tune-up',
            'status': 'completed',
            'priority': 'medium',
            'due_date': date.today() - timedelta(days=13),
            'current_mileage': 156000,
            'due_mileage': 155000,
            'estimated_cost': 750.0,
            'assigned_to': 'Service Center B'
        }
    ]
    
    for data in sample_data:
        item = MaintenanceItem(**data)
        db.session.add(item)
    
    db.session.commit()
    print(f"Seeded {len(sample_data)} maintenance items successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
