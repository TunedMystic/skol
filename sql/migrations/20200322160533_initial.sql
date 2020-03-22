-- migrate:up
CREATE TABLE IF NOT EXISTS _user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);


-- migrate:down
