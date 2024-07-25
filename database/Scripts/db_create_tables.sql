CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    state VARCHAR(1) NOT NULL DEFAULT 'A',  -- Estado: 'A' para activo, 'I' para inactivo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,  -- Usuario que creó el registro
    updated_by VARCHAR(50) NOT NULL   -- Usuario que actualizó el registro
);
