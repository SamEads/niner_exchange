-- Reset tables
TRUNCATE TABLE Friendships RESTART IDENTITY;
TRUNCATE TABLE Ratings RESTART IDENTITY;
TRUNCATE TABLE Listings RESTART IDENTITY;
TRUNCATE TABLE Users RESTART IDENTITY CASCADE;

-- Insert initial users
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

-- Generate additional users up to 500
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

-- Add 10 friends to jdoe's friends list
DO $$
DECLARE
    user_id_jdoe INT;
    random_user_id INT;
BEGIN
    -- Get jdoe's user ID
    SELECT id INTO user_id_jdoe FROM Users WHERE username = 'jdoe';

    -- Add 10 unique friends for jdoe
    FOR i IN 1..10 LOOP
        LOOP
            -- Select a random user who is not already a friend and not jdoe
            SELECT id INTO random_user_id
            FROM Users
            WHERE id != user_id_jdoe
              AND id NOT IN (
                  SELECT friend_id FROM Friendships WHERE user_id = user_id_jdoe
              )
              ORDER BY RANDOM()
              LIMIT 1;

            EXIT WHEN random_user_id IS NOT NULL;

        END LOOP;

        -- Insert friendship for jdoe
        INSERT INTO Friendships (user_id, friend_id, status)
        VALUES (user_id_jdoe, random_user_id, 'accepted');

        -- Insert reciprocal friendship for the friend
        INSERT INTO Friendships (user_id, friend_id, status)
        VALUES (random_user_id, user_id_jdoe, 'accepted');
    END LOOP;
END $$;

-- Add 10 friends to asmith's friends list
DO $$
DECLARE
    user_id_asmith INT;
    random_user_id INT;
BEGIN
    -- Get asmith's user ID
    SELECT id INTO user_id_asmith FROM Users WHERE username = 'asmith';

    -- Add 10 unique friends for asmith
    FOR i IN 1..10 LOOP
        LOOP
            -- Select a random user who is not already a friend and not asmith
            SELECT id INTO random_user_id
            FROM Users
            WHERE id != user_id_asmith
              AND id NOT IN (
                  SELECT friend_id FROM Friendships WHERE user_id = user_id_asmith
              )
              ORDER BY RANDOM()
              LIMIT 1;

            EXIT WHEN random_user_id IS NOT NULL;

        END LOOP;

        -- Insert friendship for asmith
        INSERT INTO Friendships (user_id, friend_id, status)
        VALUES (user_id_asmith, random_user_id, 'accepted');

        -- Insert reciprocal friendship for the friend
        INSERT INTO Friendships (user_id, friend_id, status)
        VALUES (random_user_id, user_id_asmith, 'accepted');
    END LOOP;
END $$;

-- Verify jdoe's friends
SELECT u.username AS friend_username
FROM Friendships f
JOIN Users u ON f.friend_id = u.id
WHERE f.user_id = (SELECT id FROM Users WHERE username = 'jdoe') AND f.status = 'accepted';

-- Verify asmith's friends
SELECT u.username AS friend_username
FROM Friendships f
JOIN Users u ON f.friend_id = u.id
WHERE f.user_id = (SELECT id FROM Users WHERE username = 'asmith') AND f.status = 'accepted';
