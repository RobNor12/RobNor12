-- Drop tables and indices if they already exist to allow safe re-creation
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- Creates the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

-- Creates the transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    transacted_at DATETIME NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Creates a unique index on the username field for quick lookups
CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);
