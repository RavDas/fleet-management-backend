-- Create drivers table
CREATE TABLE drivers (
    driver_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    license_number VARCHAR(255) NOT NULL UNIQUE,
    expiry_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create forms table
CREATE TABLE forms (
    form_id BIGSERIAL PRIMARY KEY,
    driver_id BIGINT NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    vehicle_number VARCHAR(255) NOT NULL,
    score DOUBLE PRECISION,
    fuel_efficiency DOUBLE PRECISION,
    on_time_rate DOUBLE PRECISION,
    vehicle_id BIGINT
);

-- Create schedules table
CREATE TABLE schedules (
    schedule_id BIGSERIAL PRIMARY KEY,
    driver_id VARCHAR(255) NOT NULL,
    route VARCHAR(255) NOT NULL,
    vehicle TEXT,
    status VARCHAR(255) NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);
