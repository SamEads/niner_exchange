-- Set session to replica to disable foreign key checks during truncation
SET session_replication_role = replica;

-- Wipe all tables with CASCADE to remove all related records
TRUNCATE TABLE public.Users CASCADE;
TRUNCATE TABLE public.Listings CASCADE;
TRUNCATE TABLE public.Ratings CASCADE;
TRUNCATE TABLE public.Messages CASCADE;
TRUNCATE TABLE public.Uploads CASCADE;
TRUNCATE TABLE public.Friendships CASCADE;

-- Reset sequences for SERIAL columns to start from 1
ALTER SEQUENCE public.Users_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Listings_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Ratings_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Messages_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Uploads_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Friendships_id_seq RESTART WITH 1;

-- Re-enable foreign key checks by restoring session replication role
SET session_replication_role = origin;

-- Optional: Verify that tables are empty and sequences are reset
SELECT table_name,
       (SELECT count(*) FROM information_schema.columns WHERE table_name = table_name) AS column_count
FROM information_schema.tables WHERE table_schema = 'public';

-- Verify sequence values
SELECT
    pg_get_serial_sequence('public.Users', 'id'),
    pg_get_serial_sequence('public.Listings', 'id'),
    pg_get_serial_sequence('public.Ratings', 'id'),
    pg_get_serial_sequence('public.Messages', 'id'),
    pg_get_serial_sequence('public.Uploads', 'id'),
    pg_get_serial_sequence('public.Friendships', 'id');
