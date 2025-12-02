-- Add vehicle_id column to schedules table
ALTER TABLE schedules ADD COLUMN vehicle_id VARCHAR(255);

-- Migrate data from JSON vehicle column if possible (optional, assuming new starts blank)
-- UPDATE schedules SET vehicle_id = (vehicle::jsonb->>'id') WHERE vehicle IS NOT NULL;

-- Drop the old vehicle JSON column
ALTER TABLE schedules DROP COLUMN vehicle;

