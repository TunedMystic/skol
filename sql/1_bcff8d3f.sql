CREATE TABLE IF NOT EXISTS _country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS _event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(100),
    tagline VARCHAR(100),
    date DATE,

    -- Foreign key relations.
    country_id INTEGER REFERENCES _country(id)
);
