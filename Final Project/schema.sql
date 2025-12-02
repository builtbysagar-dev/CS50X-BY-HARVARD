CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    entertainment_budget REAL DEFAULT 50.0,
    productivity_budget REAL DEFAULT 100.0
);

CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    category TEXT NOT NULL,
    renewal_date DATE NOT NULL,
    billing_cycle TEXT DEFAULT 'Monthly',
    cancel_url TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
