-- ===============================
-- Maintenance Service Database Schema
-- PostgreSQL Initialization Script
-- ===============================

-- Create database if not exists (already done by docker-compose)
-- This script runs automatically when the container starts

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create maintenance_items table
-- Schema matches the existing SQLite database structure
CREATE TABLE IF NOT EXISTS maintenance_items (
    id VARCHAR(50) PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    
    -- Dates
    due_date DATE NOT NULL,
    scheduled_date TIMESTAMP,
    completed_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Mileage
    current_mileage INTEGER NOT NULL,
    due_mileage INTEGER NOT NULL,
    
    -- Cost
    estimated_cost FLOAT DEFAULT 0.0,
    actual_cost FLOAT,
    
    -- Assignment
    assigned_to VARCHAR(200),
    assigned_technician VARCHAR(100),
    
    -- Additional info
    notes TEXT,
    parts_needed JSONB,
    attachments JSONB,
    
    -- Constraints
    CONSTRAINT chk_status CHECK (status IN ('overdue', 'due_soon', 'scheduled', 'in_progress', 'completed', 'cancelled')),
    CONSTRAINT chk_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_vehicle_id ON maintenance_items(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_status ON maintenance_items(status);
CREATE INDEX IF NOT EXISTS idx_priority ON maintenance_items(priority);
CREATE INDEX IF NOT EXISTS idx_due_date ON maintenance_items(due_date);
CREATE INDEX IF NOT EXISTS idx_created_at ON maintenance_items(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updated_at
DROP TRIGGER IF EXISTS update_maintenance_items_updated_at ON maintenance_items;
CREATE TRIGGER update_maintenance_items_updated_at
    BEFORE UPDATE ON maintenance_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO maintenance_items (id, vehicle_id, type, status, priority, due_date, current_mileage, due_mileage, estimated_cost, assigned_to, description)
VALUES
    ('M001', 'VH-001', 'Oil Change', 'overdue', 'high', CURRENT_DATE - INTERVAL '8 days', 45230, 45000, 150.0, 'Service Center A', 'Regular oil and filter change needed'),
    ('M002', 'VH-002', 'Brake Inspection', 'in_progress', 'medium', CURRENT_DATE + INTERVAL '3 days', 67890, 68000, 300.0, 'Service Center B', 'Annual brake system check'),
    ('M003', 'VH-003', 'Tire Rotation', 'scheduled', 'low', CURRENT_DATE + INTERVAL '10 days', 23456, 25000, 80.0, 'Service Center A', 'Rotate all four tires'),
    ('M004', 'VH-001', 'Annual Inspection', 'due_soon', 'high', CURRENT_DATE + INTERVAL '2 days', 89123, 90000, 500.0, 'Service Center C', 'Comprehensive annual vehicle inspection'),
    ('M005', 'VH-002', 'Engine Tune-up', 'completed', 'medium', CURRENT_DATE - INTERVAL '13 days', 156000, 155000, 750.0, 'Service Center B', 'Complete engine diagnostic and tune-up')
ON CONFLICT (id) DO NOTHING;

-- Display confirmation message
DO $$
BEGIN
    RAISE NOTICE '✅ Maintenance Database Schema Created Successfully!';
    RAISE NOTICE '📊 Sample data inserted: 5 maintenance items';
    RAISE NOTICE '🔧 Tables: maintenance_items';
    RAISE NOTICE '📈 Indexes: vehicle_id, status, priority, due_date, created_at';
END $$;

