-- Fictional Passport Database Schema

-- ----------------------------------------------------
-- 1. USERS Table
-- Stores user credentials for login and authentication.
-- ----------------------------------------------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    -- Optional: Tracks when the user registered
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------
-- 2. STAMPS Table
-- Stores all recorded fictional and real travel stamps.
-- ----------------------------------------------------
CREATE TABLE stamps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Link to the user who created the stamp
    user_id INTEGER NOT NULL,
    
    -- Location details
    location_type TEXT NOT NULL,      -- 'real' or 'fictional'
    location_name TEXT NOT NULL,
    source TEXT NOT NULL,             -- Book/Movie/Series Title
    means TEXT NOT NULL,              -- Media Type (book, movie, tvseries, etc.)
    
    -- Geographic data
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    
    -- Timestamp for history ordering
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint
    FOREIGN KEY (user_id) REFERENCES users(id)
);