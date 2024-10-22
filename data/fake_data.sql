TRUNCATE TABLE Ratings RESTART IDENTITY;
TRUNCATE Table listings RESTART IDENTITY ;
TRUNCATE TABLE Users RESTART IDENTITY CASCADE ;

select * from users;
select * from ratings;

INSERT INTO Users (username, first_name, email, password_hash, class_level) VALUES
('jdoe', 'John', 'jdoe@example.com', '$2y$12$FOIyR6PWmanG4pbVJw4tmOsA4zPrFOVTaDtEcX9qkFU0rwjOM/GEu', 1), -- login with this, user shoudl have 4 stars : hashed_password_1
('asmith', 'Alice', 'asmith@example.com', 'hashed_password_2', 2),
('bking', 'Bob', 'bking@example.com', 'hashed_password_3', 3),
('csanders', 'Charlie', 'csanders@example.com', 'hashed_password_4', 4),
('dmartin', 'Diana', 'dmartin@example.com', 'hashed_password_5', 1),
('ewilliams', 'Eve', 'ewilliams@example.com', 'hashed_password_6', 2),
('fthompson', 'Frank', 'fthompson@example.com', 'hashed_password_7', 3),
('gclark', 'Grace', 'gclark@example.com', 'hashed_password_8', 4),
('hlee', 'Hank', 'hlee@example.com', 'hashed_password_9', 1),
('ijones', 'Ivy', 'ijones@example.com', 'hashed_password_10', 2);

-- Insert fake ratings
INSERT INTO Ratings (user_id, rater_id, rating) VALUES
(1, 2, 5),  -- John rated by Alice
(1, 3, 3),  -- John rated by Bob
(1, 4, 4),  -- John rated by Charlie
(2, 1, 4),  -- Alice rated by John
(2, 5, 3),  -- Alice rated by Diana
(3, 1, 2),  -- Bob rated by John
(3, 2, 4),  -- Bob rated by Alice
(4, 3, 5),  -- Charlie rated by Bob
(5, 6, 2),  -- Diana rated by Eve
(6, 7, 3),  -- Eve rated by Frank
(7, 8, 4),  -- Frank rated by Grace
(8, 9, 5),  -- Grace rated by Hank
(9, 10, 1), -- Hank rated by Ivy
(10, 1, 3); -- Ivy rated by John

select * from users;