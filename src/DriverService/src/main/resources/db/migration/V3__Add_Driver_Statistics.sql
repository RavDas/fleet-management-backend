-- Add driver statistics columns
ALTER TABLE drivers ADD COLUMN star_rating DOUBLE PRECISION DEFAULT 4.5;
ALTER TABLE drivers ADD COLUMN trip_count INTEGER DEFAULT 0;
ALTER TABLE drivers ADD COLUMN hours_this_week DOUBLE PRECISION DEFAULT 0.0;

-- Add comments for clarity
COMMENT ON COLUMN drivers.star_rating IS 'Driver performance rating (0-5 stars)';
COMMENT ON COLUMN drivers.trip_count IS 'Total number of completed trips';
COMMENT ON COLUMN drivers.hours_this_week IS 'Hours worked in the current week';

