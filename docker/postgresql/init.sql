DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'travel_planner') THEN
        CREATE DATABASE travel_planner;
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE travel_planner TO admin;