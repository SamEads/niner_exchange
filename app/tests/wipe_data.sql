
SET session_replication_role = replica;

-- Wipe all tables
TRUNCATE TABLE public.Users CASCADE;
TRUNCATE TABLE public.Listings CASCADE;
TRUNCATE TABLE public.Ratings CASCADE;
TRUNCATE TABLE public.Messages CASCADE;
TRUNCATE TABLE public.Uploads CASCADE;

-- Reset sequences for SERIAL columns
ALTER SEQUENCE public.Users_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Listings_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Ratings_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Messages_id_seq RESTART WITH 1;
ALTER SEQUENCE public.Uploads_id_seq RESTART WITH 1;

-- Re-enable foreign key checks
SET session_replication_role = origin;
