-- Reset tables
TRUNCATE TABLE Ratings RESTART IDENTITY;
TRUNCATE TABLE Listings RESTART IDENTITY;
TRUNCATE TABLE Users RESTART IDENTITY CASCADE;
TRUNCATE TABLE ratings RESTART IDENTITY;

-- Insert users
INSERT INTO Users (username, first_name, email, password_hash, class_level) VALUES
('jdoe', 'John', 'jdoe@example.com', '$2y$12$FOIyR6PWmanG4pbVJw4tmOsA4zPrFOVTaDtEcX9qkFU0rwjOM/GEu', 1), -- Hashed password example
('asmith', 'Alice', 'asmith@example.com', 'hashed_password_2', 2),
('bking', 'Bob', 'bking@example.com', 'hashed_password_3', 3),
('csanders', 'Charlie', 'csanders@example.com', 'hashed_password_4', 4),
('dmartin', 'Diana', 'dmartin@example.com', 'hashed_password_5', 1),
('ewilliams', 'Eve', 'ewilliams@example.com', 'hashed_password_6', 2),
('fthompson', 'Frank', 'fthompson@example.com', 'hashed_password_7', 3),
('gclark', 'Grace', 'gclark@example.com', 'hashed_password_8', 4),
('hlee', 'Hank', 'hlee@example.com', 'hashed_password_9', 1),
('ijones', 'Ivy', 'ijones@example.com', 'hashed_password_10', 2);

-- Generate additional user records up to 500
DO $$
BEGIN
    FOR i IN 11..500 LOOP
        INSERT INTO Users (username, first_name, email, password_hash, class_level)
        VALUES (
            'user' || i,
            'User' || i,
            'user' || i || '@example.com',
            'hashed_password_' || i,
            (i % 4) + 1
        );
    END LOOP;
END $$;

-- Insert ratings for initial users
INSERT INTO Ratings (user_id, rater_id, rating) VALUES
(1, 2, 5), (1, 3, 3), (1, 4, 4),
(2, 1, 4), (2, 5, 3), (3, 1, 2),
(3, 2, 4), (4, 3, 5), (5, 6, 2),
(6, 7, 3), (7, 8, 4), (8, 9, 5),
(9, 10, 1), (10, 1, 3);

-- Generate additional random ratings
DO $$
BEGIN
    FOR i IN 1..5000 LOOP
        INSERT INTO Ratings (user_id, rater_id, rating)
        VALUES (
            (FLOOR(random() * 500 + 1))::int,  -- Random user_id between 1 and 500
            (FLOOR(random() * 500 + 1))::int,  -- Random rater_id between 1 and 500
            FLOOR((random() * 5 + 1))::int     -- Random rating between 1 and 5
        )
        ON CONFLICT DO NOTHING;
    END LOOP;
END $$;

-- Select to verify data
SELECT * FROM Users LIMIT 10;
SELECT * FROM Ratings LIMIT 10;
