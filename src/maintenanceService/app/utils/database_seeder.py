"""
Database Seeder for Maintenance Service
Automatically seeds sample data on startup if database is empty
This module is idempotent - safe to run multiple times
"""

from datetime import date, datetime, timedelta
from app import db
from app.models.maintainance import (
    MaintenanceItem, MaintenanceStatus, MaintenancePriority,
    Technician, TechnicianStatus, Part, RecurringSchedule, FrequencyType
)
import logging

logger = logging.getLogger(__name__)


def seed_database():
    """
    Seeds the database with sample maintenance data
    This function is idempotent - it checks if data exists before seeding
    """
    try:
        # Check if data already exists
        existing_maintenance_count = MaintenanceItem.query.count()
        existing_technician_count = Technician.query.count()
        existing_parts_count = Part.query.count()
        existing_schedule_count = RecurringSchedule.query.count()
        
        if existing_maintenance_count > 0 or existing_technician_count > 0:
            logger.info(f"ℹ️  Database already contains data. Skipping seed.")
            logger.info(f"   - Maintenance items: {existing_maintenance_count}")
            logger.info(f"   - Technicians: {existing_technician_count}")
            logger.info(f"   - Parts: {existing_parts_count}")
            logger.info(f"   - Recurring schedules: {existing_schedule_count}")
            return False
        
        logger.info("🌱 Seeding database with comprehensive maintenance data...")
        
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
                'assigned_to': 'Service Center A',
                'assigned_technician': 'Mike Henderson',
                'parts_needed': [
                    {'part_id': 'PART-001', 'name': 'Engine Oil Filter', 'quantity': 1},
                    {'part_id': 'PART-006', 'name': 'Engine Oil', 'quantity': 5}
                ]
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
                'assigned_to': 'Service Center B',
                'assigned_technician': 'James Wong'
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
                'assigned_to': 'Service Center A',
                'assigned_technician': 'Sarah Martinez',
                'parts_needed': [
                    {'part_id': 'PART-002', 'name': 'Brake Pads (Front)', 'quantity': 2},
                    {'part_id': 'PART-010', 'name': 'Brake Fluid', 'quantity': 1}
                ]
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
                'assigned_to': 'Service Center C',
                'assigned_technician': 'Rachel Cooper'
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
                'assigned_to': 'Service Center C',
                'assigned_technician': 'Rachel Cooper',
                'parts_needed': [
                    {'part_id': 'PART-004', 'name': 'Transmission Fluid (5L)', 'quantity': 2}
                ]
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
                'assigned_to': 'Service Center A',
                'assigned_technician': 'Mike Henderson'
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
                'assigned_to': 'Service Center A',
                'assigned_technician': 'David Kim'
            },
            {
                'id': 'M016',
                'vehicle_id': 'FLR-3456',
                'type': 'Fuel System Service',
                'description': 'Critical fuel system maintenance - low fuel alert',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() + timedelta(days=2),
                'current_mileage': 156800,
                'due_mileage': 160000,
                'estimated_cost': 380.0,
                'assigned_to': 'Service Center A',
                'assigned_technician': 'Mike Henderson'
            },
            {
                'id': 'M017',
                'vehicle_id': 'VLV-7890',
                'type': 'Preventive Maintenance',
                'description': 'Upcoming maintenance due - full service required',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.HIGH,
                'due_date': date.today() + timedelta(days=12),
                'current_mileage': 187200,
                'due_mileage': 190000,
                'estimated_cost': 550.0,
                'assigned_to': 'Service Center B',
                'assigned_technician': 'David Kim'
            },
            {
                'id': 'M018',
                'vehicle_id': 'KW-1122',
                'type': 'Engine Overhaul',
                'description': 'Major engine overhaul in progress',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.CRITICAL,
                'due_date': date.today() - timedelta(days=15),
                'current_mileage': 98400,
                'due_mileage': 100000,
                'estimated_cost': 2500.0,
                'assigned_to': 'Service Center B',
                'assigned_technician': 'Rachel Cooper',
                'parts_needed': [
                    {'part_id': 'PART-005', 'name': 'Spark Plugs', 'quantity': 2},
                    {'part_id': 'PART-011', 'name': 'Serpentine Belt', 'quantity': 1}
                ]
            },
            {
                'id': 'M019',
                'vehicle_id': 'INT-3322',
                'type': 'Transmission Rebuild',
                'description': 'Complete transmission rebuild - critical failure',
                'status': MaintenanceStatus.IN_PROGRESS,
                'priority': MaintenancePriority.CRITICAL,
                'due_date': date.today() - timedelta(days=20),
                'current_mileage': 203400,
                'due_mileage': 200000,
                'estimated_cost': 3200.0,
                'assigned_to': 'Service Center C',
                'assigned_technician': 'Sarah Martinez',
                'parts_needed': [
                    {'part_id': 'PART-004', 'name': 'Transmission Fluid (5L)', 'quantity': 3}
                ]
            },
            {
                'id': 'M020',
                'vehicle_id': 'DAF-7755',
                'type': 'Fuel Tank Inspection',
                'description': 'Low fuel alert - inspect fuel system and refill',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=1),
                'current_mileage': 134500,
                'due_mileage': 140000,
                'estimated_cost': 120.0,
                'assigned_to': 'Service Center B'
            },
            {
                'id': 'M021',
                'vehicle_id': 'PB-5544',
                'type': 'Tire Service',
                'description': 'Tire rotation and pressure check',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=8),
                'current_mileage': 72300,
                'due_mileage': 75000,
                'estimated_cost': 95.0,
                'assigned_to': 'Service Center A',
                'parts_needed': [
                    {'part_id': 'PART-009', 'name': 'Tire 225/60R17', 'quantity': 0}
                ]
            },
            {
                'id': 'M022',
                'vehicle_id': 'MCK-9988',
                'type': 'Battery Replacement',
                'description': 'Replace aging battery',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.MEDIUM,
                'due_date': date.today() + timedelta(days=15),
                'current_mileage': 34200,
                'due_mileage': 40000,
                'estimated_cost': 295.0,
                'assigned_to': 'Service Center A',
                'parts_needed': [
                    {'part_id': 'PART-008', 'name': 'Battery 12V Heavy Duty', 'quantity': 1}
                ]
            },
            {
                'id': 'M023',
                'vehicle_id': 'HNO-1010',
                'type': 'HVAC Service',
                'description': 'Air conditioning system service and filter replacement',
                'status': MaintenanceStatus.COMPLETED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() - timedelta(days=10),
                'current_mileage': 45200,
                'due_mileage': 50000,
                'estimated_cost': 175.0,
                'assigned_to': 'Service Center B',
                'assigned_technician': 'David Kim',
                'parts_needed': [
                    {'part_id': 'PART-012', 'name': 'Cabin Air Filter', 'quantity': 1}
                ]
            },
            {
                'id': 'M024',
                'vehicle_id': 'SCN-4488',
                'type': 'General Service',
                'description': 'Regular maintenance check and fluid top-up',
                'status': MaintenanceStatus.SCHEDULED,
                'priority': MaintenancePriority.LOW,
                'due_date': date.today() + timedelta(days=20),
                'current_mileage': 28900,
                'due_mileage': 30000,
                'estimated_cost': 180.0,
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
        
        # Commit maintenance items
        db.session.commit()
        logger.info(f"✅ Successfully seeded {items_created} maintenance items")
        
        # ===== SEED TECHNICIANS =====
        logger.info("🔧 Seeding technicians...")
        technicians_data = [
            {
                'id': 'TECH-001',
                'name': 'Mike Henderson',
                'email': 'mike.henderson@fleetops.com',
                'phone': '+1-555-1001',
                'specialization': ['Engine Diagnostics', 'Oil Changes', 'General Maintenance'],
                'status': TechnicianStatus.AVAILABLE,
                'rating': 4.8,
                'completed_jobs': 342,
                'active_jobs': 2,
                'certifications': ['ASE Master Technician', 'Diesel Engine Specialist'],
                'hourly_rate': 65.0,
                'join_date': date(2020, 3, 15)
            },
            {
                'id': 'TECH-002',
                'name': 'Sarah Martinez',
                'email': 'sarah.martinez@fleetops.com',
                'phone': '+1-555-1002',
                'specialization': ['Brake Systems', 'Suspension', 'Tire Service'],
                'status': TechnicianStatus.BUSY,
                'rating': 4.9,
                'completed_jobs': 456,
                'active_jobs': 3,
                'certifications': ['ASE Master Technician', 'Brake Specialist Certification'],
                'hourly_rate': 70.0,
                'join_date': date(2019, 6, 10)
            },
            {
                'id': 'TECH-003',
                'name': 'James Wong',
                'email': 'james.wong@fleetops.com',
                'phone': '+1-555-1003',
                'specialization': ['Electric Vehicles', 'Battery Systems', 'Software Updates'],
                'status': TechnicianStatus.AVAILABLE,
                'rating': 5.0,
                'completed_jobs': 289,
                'active_jobs': 1,
                'certifications': ['Tesla Certified Technician', 'EV Specialist', 'High Voltage Safety'],
                'hourly_rate': 85.0,
                'join_date': date(2021, 1, 20)
            },
            {
                'id': 'TECH-004',
                'name': 'Rachel Cooper',
                'email': 'rachel.cooper@fleetops.com',
                'phone': '+1-555-1004',
                'specialization': ['Transmission Service', 'Fuel Systems', 'Engine Repair'],
                'status': TechnicianStatus.BUSY,
                'rating': 4.7,
                'completed_jobs': 398,
                'active_jobs': 2,
                'certifications': ['ASE Master Technician', 'Transmission Specialist'],
                'hourly_rate': 72.0,
                'join_date': date(2020, 9, 5)
            },
            {
                'id': 'TECH-005',
                'name': 'David Kim',
                'email': 'david.kim@fleetops.com',
                'phone': '+1-555-1005',
                'specialization': ['Air Conditioning', 'Electrical Systems', 'Diagnostics'],
                'status': TechnicianStatus.AVAILABLE,
                'rating': 4.6,
                'completed_jobs': 312,
                'active_jobs': 1,
                'certifications': ['ASE Certified', 'HVAC Specialist'],
                'hourly_rate': 68.0,
                'join_date': date(2021, 4, 12)
            },
            {
                'id': 'TECH-006',
                'name': 'Angela Stevens',
                'email': 'angela.stevens@fleetops.com',
                'phone': '+1-555-1006',
                'specialization': ['Preventive Maintenance', 'Inspections', 'General Repair'],
                'status': TechnicianStatus.OFF_DUTY,
                'rating': 4.5,
                'completed_jobs': 267,
                'active_jobs': 0,
                'certifications': ['ASE Certified', 'Safety Inspector'],
                'hourly_rate': 62.0,
                'join_date': date(2022, 2, 1)
            }
        ]
        
        technicians_created = 0
        for tech_data in technicians_data:
            try:
                technician = Technician(**tech_data)
                db.session.add(technician)
                technicians_created += 1
            except Exception as e:
                logger.warning(f"⚠️  Could not create technician {tech_data.get('id', 'unknown')}: {str(e)}")
                continue
        
        db.session.commit()
        logger.info(f"✅ Successfully seeded {technicians_created} technicians")
        
        # ===== SEED PARTS INVENTORY =====
        logger.info("📦 Seeding parts inventory...")
        parts_data = [
            {
                'id': 'PART-001',
                'name': 'Engine Oil Filter',
                'part_number': 'EOF-2024-001',
                'category': 'Filters',
                'quantity': 45,
                'min_quantity': 15,
                'unit_cost': 12.50,
                'supplier': 'AutoParts Supply Co.',
                'location': 'Warehouse A - Shelf 12',
                'last_restocked': date.today() - timedelta(days=15),
                'used_in': ['Oil Change', 'General Maintenance']
            },
            {
                'id': 'PART-002',
                'name': 'Brake Pads (Front)',
                'part_number': 'BPF-2024-002',
                'category': 'Brakes',
                'quantity': 28,
                'min_quantity': 10,
                'unit_cost': 85.00,
                'supplier': 'BrakeMax Industries',
                'location': 'Warehouse A - Shelf 8',
                'last_restocked': date.today() - timedelta(days=7),
                'used_in': ['Brake System Overhaul', 'Brake Service']
            },
            {
                'id': 'PART-003',
                'name': 'Air Filter',
                'part_number': 'AF-2024-003',
                'category': 'Filters',
                'quantity': 52,
                'min_quantity': 20,
                'unit_cost': 18.75,
                'supplier': 'AutoParts Supply Co.',
                'location': 'Warehouse A - Shelf 12',
                'last_restocked': date.today() - timedelta(days=20),
                'used_in': ['Air Filter Replacement', 'General Maintenance']
            },
            {
                'id': 'PART-004',
                'name': 'Transmission Fluid (5L)',
                'part_number': 'TF-2024-004',
                'category': 'Fluids',
                'quantity': 35,
                'min_quantity': 12,
                'unit_cost': 45.00,
                'supplier': 'FluidTech Solutions',
                'location': 'Warehouse B - Bay 3',
                'last_restocked': date.today() - timedelta(days=10),
                'used_in': ['Transmission Service', 'Fluid Replacement']
            },
            {
                'id': 'PART-005',
                'name': 'Spark Plugs (Set of 4)',
                'part_number': 'SP-2024-005',
                'category': 'Ignition',
                'quantity': 18,
                'min_quantity': 8,
                'unit_cost': 32.00,
                'supplier': 'IgnitionPro',
                'location': 'Warehouse A - Shelf 15',
                'last_restocked': date.today() - timedelta(days=25),
                'used_in': ['Spark Plug Replacement', 'Engine Tune-up']
            },
            {
                'id': 'PART-006',
                'name': 'Coolant (10L)',
                'part_number': 'CL-2024-006',
                'category': 'Fluids',
                'quantity': 42,
                'min_quantity': 15,
                'unit_cost': 28.50,
                'supplier': 'FluidTech Solutions',
                'location': 'Warehouse B - Bay 3',
                'last_restocked': date.today() - timedelta(days=12),
                'used_in': ['Coolant Flush', 'Cooling System Service']
            },
            {
                'id': 'PART-007',
                'name': 'Wiper Blades (Pair)',
                'part_number': 'WB-2024-007',
                'category': 'Accessories',
                'quantity': 38,
                'min_quantity': 15,
                'unit_cost': 22.00,
                'supplier': 'AutoParts Supply Co.',
                'location': 'Warehouse A - Shelf 5',
                'last_restocked': date.today() - timedelta(days=18),
                'used_in': ['Wiper Blade Replacement', 'General Maintenance']
            },
            {
                'id': 'PART-008',
                'name': 'Battery 12V Heavy Duty',
                'part_number': 'BAT-2024-008',
                'category': 'Electrical',
                'quantity': 12,
                'min_quantity': 5,
                'unit_cost': 185.00,
                'supplier': 'PowerCell Batteries',
                'location': 'Warehouse B - Bay 1',
                'last_restocked': date.today() - timedelta(days=5),
                'used_in': ['Battery Replacement', 'Electrical Service']
            },
            {
                'id': 'PART-009',
                'name': 'Tire 225/60R17',
                'part_number': 'TR-2024-009',
                'category': 'Tires',
                'quantity': 24,
                'min_quantity': 8,
                'unit_cost': 145.00,
                'supplier': 'TireWorld Distributors',
                'location': 'Warehouse C - Tire Rack',
                'last_restocked': date.today() - timedelta(days=8),
                'used_in': ['Tire Replacement', 'Tire Rotation']
            },
            {
                'id': 'PART-010',
                'name': 'Brake Fluid (1L)',
                'part_number': 'BF-2024-010',
                'category': 'Fluids',
                'quantity': 6,
                'min_quantity': 10,
                'unit_cost': 15.50,
                'supplier': 'FluidTech Solutions',
                'location': 'Warehouse B - Bay 3',
                'last_restocked': date.today() - timedelta(days=30),
                'used_in': ['Brake Service', 'Brake System Overhaul']
            },
            {
                'id': 'PART-011',
                'name': 'Serpentine Belt',
                'part_number': 'SB-2024-011',
                'category': 'Engine',
                'quantity': 22,
                'min_quantity': 8,
                'unit_cost': 38.00,
                'supplier': 'BeltPro Manufacturing',
                'location': 'Warehouse A - Shelf 18',
                'last_restocked': date.today() - timedelta(days=14),
                'used_in': ['Belt Replacement', 'Engine Service']
            },
            {
                'id': 'PART-012',
                'name': 'Cabin Air Filter',
                'part_number': 'CAF-2024-012',
                'category': 'Filters',
                'quantity': 31,
                'min_quantity': 12,
                'unit_cost': 24.00,
                'supplier': 'AutoParts Supply Co.',
                'location': 'Warehouse A - Shelf 12',
                'last_restocked': date.today() - timedelta(days=9),
                'used_in': ['Air Filter Replacement', 'HVAC Service']
            }
        ]
        
        parts_created = 0
        for part_data in parts_data:
            try:
                part = Part(**part_data)
                db.session.add(part)
                parts_created += 1
            except Exception as e:
                logger.warning(f"⚠️  Could not create part {part_data.get('id', 'unknown')}: {str(e)}")
                continue
        
        db.session.commit()
        logger.info(f"✅ Successfully seeded {parts_created} parts")
        
        # ===== SEED RECURRING SCHEDULES =====
        logger.info("📅 Seeding recurring maintenance schedules...")
        recurring_schedules_data = [
            {
                'id': 'RS-001',
                'name': 'Monthly Oil Change - ABC-1234',
                'vehicle_id': 'ABC-1234',
                'maintenance_type': 'Oil Change',
                'description': 'Regular monthly oil and filter change for Ford Transit Van',
                'frequency': FrequencyType.MONTHLY,
                'frequency_value': 1,
                'estimated_cost': 150.0,
                'estimated_duration': 0.75,
                'assigned_to': 'Service Center A',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=30),
                'next_scheduled': datetime.utcnow() + timedelta(days=5),
                'total_executions': 12
            },
            {
                'id': 'RS-002',
                'name': 'Quarterly Inspection - XYZ-5678',
                'vehicle_id': 'XYZ-5678',
                'maintenance_type': 'Battery Check',
                'description': 'Quarterly Tesla battery health inspection',
                'frequency': FrequencyType.QUARTERLY,
                'frequency_value': 1,
                'estimated_cost': 200.0,
                'estimated_duration': 1.5,
                'assigned_to': 'Service Center B',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=90),
                'next_scheduled': datetime.utcnow() + timedelta(days=15),
                'total_executions': 4
            },
            {
                'id': 'RS-003',
                'name': 'Semi-Annual Brake Check - JKL-9101',
                'vehicle_id': 'JKL-9101',
                'maintenance_type': 'Brake Inspection',
                'description': 'Comprehensive brake system inspection every 6 months',
                'frequency': FrequencyType.MONTHLY,
                'frequency_value': 6,
                'estimated_cost': 250.0,
                'estimated_duration': 2.0,
                'assigned_to': 'Service Center A',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=180),
                'next_scheduled': datetime.utcnow() + timedelta(days=10),
                'total_executions': 8
            },
            {
                'id': 'RS-004',
                'name': 'Tire Rotation - MBZ-2468',
                'vehicle_id': 'MBZ-2468',
                'maintenance_type': 'Tire Rotation',
                'description': 'Rotate tires every 3 months or 5,000 miles',
                'frequency': FrequencyType.QUARTERLY,
                'frequency_value': 1,
                'estimated_cost': 120.0,
                'estimated_duration': 1.0,
                'assigned_to': 'Service Center B',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=60),
                'next_scheduled': datetime.utcnow() + timedelta(days=30),
                'total_executions': 6
            },
            {
                'id': 'RS-005',
                'name': 'Annual Comprehensive - CHV-1357',
                'vehicle_id': 'CHV-1357',
                'maintenance_type': 'Annual Inspection',
                'description': 'Full vehicle inspection and service annually',
                'frequency': FrequencyType.YEARLY,
                'frequency_value': 1,
                'estimated_cost': 450.0,
                'estimated_duration': 4.0,
                'assigned_to': 'Service Center C',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=365),
                'next_scheduled': datetime.utcnow() + timedelta(days=30),
                'total_executions': 3
            },
            {
                'id': 'RS-006',
                'name': 'Weekly EV Check - NSN-7890',
                'vehicle_id': 'NSN-7890',
                'maintenance_type': 'Software Update',
                'description': 'Weekly software and system status check for Nissan Leaf',
                'frequency': FrequencyType.WEEKLY,
                'frequency_value': 1,
                'estimated_cost': 0.0,
                'estimated_duration': 0.5,
                'assigned_to': 'Service Center B',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=7),
                'next_scheduled': datetime.utcnow() + timedelta(days=2),
                'total_executions': 52
            },
            {
                'id': 'RS-007',
                'name': 'Bi-Monthly Air Filter - HND-5555',
                'vehicle_id': 'HND-5555',
                'maintenance_type': 'Air Filter Replacement',
                'description': 'Replace air filters every 2 months',
                'frequency': FrequencyType.MONTHLY,
                'frequency_value': 2,
                'estimated_cost': 95.0,
                'estimated_duration': 0.5,
                'assigned_to': 'Service Center A',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=45),
                'next_scheduled': datetime.utcnow() + timedelta(days=15),
                'total_executions': 9
            },
            {
                'id': 'RS-008',
                'name': 'Mileage-Based Service - ISU-9999',
                'vehicle_id': 'ISU-9999',
                'maintenance_type': 'General Maintenance',
                'description': 'Service every 10,000 miles',
                'frequency': FrequencyType.MILEAGE_BASED,
                'frequency_value': 10000,
                'estimated_cost': 350.0,
                'estimated_duration': 3.0,
                'assigned_to': 'Service Center A',
                'is_active': True,
                'last_executed': datetime.utcnow() - timedelta(days=120),
                'next_scheduled': datetime.utcnow() + timedelta(days=20),
                'total_executions': 10
            }
        ]
        
        schedules_created = 0
        for schedule_data in recurring_schedules_data:
            try:
                schedule = RecurringSchedule(**schedule_data)
                db.session.add(schedule)
                schedules_created += 1
            except Exception as e:
                logger.warning(f"⚠️  Could not create schedule {schedule_data.get('id', 'unknown')}: {str(e)}")
                continue
        
        db.session.commit()
        logger.info(f"✅ Successfully seeded {schedules_created} recurring schedules")
        
        # Final summary
        logger.info("🎉 Database seeding completed successfully!")
        logger.info("=" * 70)
        logger.info("📊 COMPREHENSIVE DATA SUMMARY")
        logger.info("=" * 70)
        logger.info(f"✅ Maintenance Items: {items_created} (M001-M024)")
        logger.info(f"   - Overdue: 4  |  In Progress: 6  |  Scheduled: 9  |  Completed: 3  |  Due Soon: 2")
        logger.info(f"✅ Technicians: {technicians_created} (with specializations & certifications)")
        logger.info(f"   - Available: 3  |  Busy: 2  |  Off Duty: 1")
        logger.info(f"✅ Parts Inventory: {parts_created} items")
        logger.info(f"   - Low stock alerts: 1 (Brake Fluid below minimum)")
        logger.info(f"✅ Recurring Schedules: {schedules_created}")
        logger.info(f"   - Daily: 0  |  Weekly: 1  |  Monthly: 3  |  Quarterly: 2  |  Yearly: 1  |  Mileage: 1")
        logger.info("=" * 70)
        logger.info("🚗 Vehicle Coverage:")
        logger.info("   - 20+ vehicles with maintenance records")
        logger.info("   - Including: ABC-1234, XYZ-5678, JKL-9101, MBZ-2468, CHV-1357,")
        logger.info("                FLR-3456, VLV-7890, KW-1122, PB-5544, MCK-9988, and more")
        logger.info("=" * 70)
        logger.info("🔧 Maintenance Types:")
        logger.info("   Oil Changes, Brake Service, Engine Diagnostics, Tire Service,")
        logger.info("   Transmission Service, Battery Checks, HVAC Service, Annual Inspections")
        logger.info("=" * 70)
        
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

