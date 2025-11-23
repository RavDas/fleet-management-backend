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
        
        # Sample maintenance items matching the init-db.sql data
        sample_data = [
            {
                'id': 'M001',
                'vehicle_id': 'VH-001',
                'type': 'Oil Change',
                'description': 'Regular oil and filter change needed',
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
                'vehicle_id': 'VH-002',
                'type': 'Brake Inspection',
                'description': 'Annual brake system check',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=3),
                'current_mileage': 67890,
                'due_mileage': 68000,
                'estimated_cost': 300.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M003',
                'vehicle_id': 'VH-003',
                'type': 'Tire Rotation',
                'description': 'Rotate all four tires',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=10),
                'current_mileage': 23456,
                'due_mileage': 25000,
                'estimated_cost': 80.0,
                'assigned_to': 'Service Center A'
            },
            {
                'id': 'M004',
                'vehicle_id': 'VH-001',
                'type': 'Annual Inspection',
                'description': 'Comprehensive annual vehicle inspection',
                'status': MaintenanceStatus.DUE_SOON,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() + timedelta(days=2),
                'current_mileage': 89123,
                'due_mileage': 90000,
                'estimated_cost': 500.0,
                'assigned_to': 'Service Center C'
            },
            {
                'id': 'M005',
                'vehicle_id': 'VH-002',
                'type': 'Engine Tune-up',
                'description': 'Complete engine diagnostic and tune-up',
                'status': MaintenanceStatus.COMPLETED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() - timedelta(days=13),
                'current_mileage': 156000,
                'due_mileage': 155000,
                'estimated_cost': 750.0,
                'assigned_to': 'Service Center B'
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
        logger.info(f"   - {items_created} maintenance items (M001-M005)")
        logger.info("   - Vehicles: VH-001, VH-002, VH-003")
        logger.info("   - Various statuses: overdue, in_progress, scheduled, due_soon, completed")
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

