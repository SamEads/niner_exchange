CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    class_level INT CHECK (class_level >= 1 AND class_level <= 4) NOT NULL, -- Class level (1-4)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Account creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);

CREATE TABLE Listings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    img BYTEA NOT NULL,
    name TEXT NOT NULL,
    mimetype TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Ratings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, -- User who is being rated
    rater_id INT NOT NULL, -- User who gave the rating
    rating INT CHECK (rating >= 1 AND rating <= 5), -- 1-5 rating system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (rater_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE (user_id, rater_id) -- Prevents the same user from rating another user multiple times
);

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    class_level INT CHECK (class_level >= 1 AND class_level <= 4) NOT NULL, -- Class level (1-4)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Account creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Last update timestamp
);

CREATE TABLE Listings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    img BYTEA NOT NULL,
    name TEXT NOT NULL,
    mimetype TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Ratings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL, -- User who is being rated
    rater_id INT NOT NULL, -- User who gave the rating
    rating INT CHECK (rating >= 1 AND rating <= 5), -- 1-5 rating system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (rater_id) REFERENCES Users(id) ON DELETE CASCADE,
    UNIQUE (user_id, rater_id) -- Prevents the same user from rating another user multiple times
);

CREATE TABLE Messages (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(255) NOT NULL,   -- Keep sender as username for consistency
    recipient VARCHAR(255) NOT NULL, -- Keep recipient as username for consistency
    content TEXT NOT NULL,
    edited BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender) REFERENCES Users(username) ON DELETE CASCADE,   -- Reference by username
    FOREIGN KEY (recipient) REFERENCES Users(username) ON DELETE CASCADE  -- Reference by username
);
