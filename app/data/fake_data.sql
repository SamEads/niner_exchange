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

TRUNCATE TABLE Listings RESTART IDENTITY;

-- Insert fake listings
INSERT INTO Listings (user_id, title, description, price, img, name, mimetype) VALUES
(1, 'Cozy Apartment Downtown', 'A cozy 1-bedroom apartment in the heart of the city.', 1200.00, 'path/to/image1.png', 'image1.png', 'image/png'),
(1, 'Spacious House with Garden', 'A beautiful 4-bedroom house with a large garden.', 2500.00, 'path/to/image2.png', 'image2.png', 'image/png'),
(2, 'Modern Studio', 'A modern studio with a stunning view.', 900.00, 'path/to/image3.png', 'image3.png', 'image/png'),
(2, 'Luxury Condo', 'A luxury condo with all amenities included.', 1800.00, 'path/to/image4.png', 'image4.png', 'image/png'),
(3, 'Charming Cottage', 'A charming 2-bedroom cottage near the park.', 1500.00, 'path/to/image5.png', 'image5.png', 'image/png'),
(3, 'Loft in Artistic Neighborhood', 'An artistic loft in a vibrant neighborhood.', 1600.00, 'path/to/image6.png', 'image6.png', 'image/png'),
(4, 'Penthouse with Rooftop', 'A stunning penthouse with a private rooftop terrace.', 3000.00, 'path/to/image7.png', 'image7.png', 'image/png'),
(5, 'Affordable Room for Rent', 'A clean room for rent in a friendly neighborhood.', 500.00, 'path/to/image8.png', 'image8.png', 'image/png'),
(6, 'Family Home with Pool', 'A spacious family home with a large swimming pool.', 2200.00, 'path/to/image9.png', 'image9.png', 'image/png'),
(7, 'Quiet Cabin in the Woods', 'A peaceful cabin for a weekend getaway.', 700.00, 'path/to/image10.png', 'image10.png', 'image/png');

-- Ensure img, name, and mimetype are now provided

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

DO $$ 
DECLARE
    user_id_jdoe INT;
    random_user_id INT;
BEGIN
    -- Get jdoe's user ID
    SELECT id INTO user_id_jdoe FROM Users WHERE username = 'jdoe';

    -- Add 10 random pending friend requests to jdoe
    FOR i IN 1..10 LOOP
        LOOP
            -- Select a random user who is not already a friend and not jdoe
            SELECT id INTO random_user_id
            FROM Users
            WHERE id != user_id_jdoe
              AND id NOT IN (
                  SELECT friend_id FROM Friendships WHERE user_id = user_id_jdoe
              )
              AND id NOT IN (
                  SELECT user_id FROM Friendships WHERE friend_id = user_id_jdoe
              )
              ORDER BY RANDOM()
              LIMIT 1;

            EXIT WHEN random_user_id IS NOT NULL;
        END LOOP;

        -- Insert a pending friendship request for jdoe
        INSERT INTO Friendships (user_id, friend_id, status)
        VALUES (random_user_id, user_id_jdoe, 'pending');
    END LOOP;
END $$;



DO $$ 
DECLARE
    user_id_jdoe INT;
    random_user_id INT;
    message_content TEXT;
BEGIN
    -- Get jdoe's user ID
    SELECT id INTO user_id_jdoe FROM Users WHERE username = 'jdoe';

    -- Generate 10 random messages for jdoe
    FOR i IN 1..10 LOOP
        LOOP
            -- Select a random user who is not jdoe
            SELECT id INTO random_user_id
            FROM Users
            WHERE id != user_id_jdoe
            ORDER BY RANDOM()
            LIMIT 1;

            EXIT WHEN random_user_id IS NOT NULL;
        END LOOP;

        -- Generate a random message content (simple example)
        message_content := 'Hello jdoe, this is a message from user ' || random_user_id || '.';

        -- Insert the message
        INSERT INTO Messages (sender, recipient, content)
        VALUES (
            (SELECT username FROM Users WHERE id = random_user_id),
            'jdoe',
            message_content
        );
    END LOOP;
END $$;
