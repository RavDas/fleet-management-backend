"""
Database Seeder for Maintenance Service
Automatically seeds sample data on startup if database is empty
This module is idempotent - safe to run multiple times
"""

from datetime import date, timedelta
from app import db
from app.models.maintainance import MaintenanceItem, MaintenanceStatus, MaintenancePriority
import logging

logger = logging.getLogger(__name__)


def seed_database():
    """
    Seeds the database with sample maintenance data
    This function is idempotent - it checks if data exists before seeding
    """
    try:
        # Check if data already exists
        existing_count = MaintenanceItem.query.count()
        if existing_count > 0:
            logger.info(f"ℹ️  Database already contains {existing_count} maintenance items. Skipping seed.")
            return False
        
        logger.info("🌱 Seeding database with sample maintenance data...")
        
        # Sample maintenance items with comprehensive coverage of all vehicles
        sample_data = [
            {
                'id': 'M001',
                'vehicle_id': 'ABC-1234',
                'type': 'Oil Change',
                'description': 'Regular oil and filter change needed - Ford Transit Van',
                'status': MaintenanceStatus.OVERDUE,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() - timedelta(days=8),
                'current_mileage': 45230,
                'due_mileage': 45000,
                'estimated_cost': 150.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M002',
                'vehicle_id': 'XYZ-5678',
                'type': 'Battery Check',
                'description': 'Tesla battery health inspection and calibration',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=3),
                'current_mileage': 13200,
                'due_mileage': 15000,
                'estimated_cost': 200.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M003',
                'vehicle_id': 'JKL-9101',
                'type': 'Brake System Overhaul',
                'description': 'Complete brake pad replacement and rotor resurfacing',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today(),
                'current_mileage': 88800,
                'due_mileage': 90000,
                'estimated_cost': 850.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M004',
                'vehicle_id': 'MBZ-2468',
                'type': 'Tire Rotation',
                'description': 'Rotate all four tires and alignment check',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=10),
                'current_mileage': 32100,
                'due_mileage': 35000,
                'estimated_cost': 120.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M005',
                'vehicle_id': 'CHV-1357',
                'type': 'Fuel System Cleaning',
                'description': 'Fuel injector cleaning and filter replacement',
                'status': MaintenanceStatus.DUE_SOON,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=5),
                'current_mileage': 67890,
                'due_mileage': 70000,
                'estimated_cost': 280.0,
                'assigned_to': 'Service Center C'
            },
            {
                'id': 'M006',
                'vehicle_id': 'NSN-7890',
                'type': 'Software Update',
                'description': 'Electric vehicle software and firmware update',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=7),
                'current_mileage': 8500,
                'due_mileage': 10000,
                'estimated_cost': 0.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M007',
                'vehicle_id': 'RAM-4321',
                'type': 'Engine Diagnostic',
                'description': 'Complete engine diagnostic - vehicle offline',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.CRITICAL,
                'due_date': date.today() - timedelta(days=7),
                'current_mileage': 102400,
                'due_mileage': 100000,
                'estimated_cost': 1200.0,
                'assigned_to': 'Service Center C'
            },
            {
                'id': 'M008',
                'vehicle_id': 'HND-5555',
                'type': 'Air Filter Replacement',
                'description': 'Replace cabin and engine air filters',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=14),
                'current_mileage': 23456,
                'due_mileage': 25000,
                'estimated_cost': 95.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M009',
                'vehicle_id': 'VW-8888',
                'type': 'Transmission Service',
                'description': 'Transmission fluid change and inspection',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() - timedelta(days=1),
                'current_mileage': 78900,
                'due_mileage': 80000,
                'estimated_cost': 650.0,
                'assigned_to': 'Service Center C'
            },
            {
                'id': 'M010',
                'vehicle_id': 'ISU-9999',
                'type': 'Annual Inspection',
                'description': 'Comprehensive annual safety inspection',
                'status': MaintenanceStatus.DUE_SOON,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() + timedelta(days=4),
                'current_mileage': 95600,
                'due_mileage': 100000,
                'estimated_cost': 450.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M011',
                'vehicle_id': 'ABC-1234',
                'type': 'Coolant Flush',
                'description': 'Complete coolant system flush and refill',
                'status': MaintenanceStatus.COMPLETED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() - timedelta(days=30),
                'current_mileage': 44000,
                'due_mileage': 45000,
                'estimated_cost': 175.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M012',
                'vehicle_id': 'XYZ-5678',
                'type': 'Tire Replacement',
                'description': 'Replace all four tires - wear detected',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() + timedelta(days=6),
                'current_mileage': 13200,
                'due_mileage': 15000,
                'estimated_cost': 1100.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M013',
                'vehicle_id': 'MBZ-2468',
                'type': 'Wiper Blade Replacement',
                'description': 'Replace front and rear wiper blades',
                'status': MaintenanceStatus.COMPLETED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() - timedelta(days=15),
                'current_mileage': 31500,
                'due_mileage': 32000,
                'estimated_cost': 45.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M014',
                'vehicle_id': 'CHV-1357',
                'type': 'Spark Plug Replacement',
                'description': 'Replace all spark plugs and ignition coils',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=20),
                'current_mileage': 67890,
                'due_mileage': 70000,
                'estimated_cost': 320.0,
                'assigned_to': 'Service Center C'
            },
            {
                'id': 'M015',
                'vehicle_id': 'HND-5555',
                'type': 'Suspension Check',
                'description': 'Inspect suspension components and shock absorbers',
                'status': MaintenanceStatus.COMPLETED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() - timedelta(days=20),
                'current_mileage': 22800,
                'due_mileage': 25000,
                'estimated_cost': 225.0,
                'assigned_to': 'Service Center A'
            }
        ]
        
        # Insert all sample data
        items_created = 0
        for data in sample_data:
            try:
                item = MaintenanceItem(**data)
                db.session.add(item)
                items_created += 1
            except Exception as e:
                logger.warning(f"⚠️  Could not create item {data.get('id', 'unknown')}: {str(e)}")
                continue
        
        # Commit all changes
        db.session.commit()
        
        logger.info(f"✅ Successfully seeded {items_created} maintenance items")
        logger.info("📊 Sample data summary:")
        logger.info(f"   - {items_created} maintenance items (M001-M015)")
        logger.info("   - Vehicles covered: ABC-1234, XYZ-5678, JKL-9101, MBZ-2468, CHV-1357, and more")
        logger.info("   - Various statuses: overdue, in_progress, scheduled, due_soon, completed, critical")
        logger.info("   - Diverse maintenance types: oil changes, brake service, diagnostics, inspections")
        logger.info("🎉 Database seeding completed successfully!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {str(e)}")
        db.session.rollback()
        raise


def initialize_database():
    """
    Initializes the database by creating tables and seeding data
    This is the main entry point called on application startup
    """
    try:
        logger.info("🔄 Initializing database...")
        
        # Create tables if they don't exist
        db.create_all()
        logger.info("✅ Database tables created/verified")
        
        # Seed data if needed
        seed_database()
        
        logger.info("✅ Database initialization complete")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

