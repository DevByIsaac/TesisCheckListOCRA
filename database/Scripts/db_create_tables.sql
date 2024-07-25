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
CREATE TABLE Empleado (
    empleado_id SERIAL PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    Nombre VARCHAR(255) NOT NULL,
    Apellido VARCHAR(255) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    edad INTEGER NOT NULL,
    puesto VARCHAR(255) NOT NULL,
    estatura FLOAT NOT NULL,
    horas_trabajo TIME NOT NULL,
    horas_descanso TIME NOT NULL,
    created_by VARCHAR(50) NOT NULL,  -- Usuario que creó el registro
    updated_by VARCHAR(50) NOT NULL   -- Usuario que actualizó el registro
);

CREATE TABLE Actividades (
    id_actividad SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    tipo_actividad VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    fecha_actividad TIMESTAMP NOT NULL,
    created_by VARCHAR(50) NOT NULL,  -- Usuario que creó el registro
    updated_by VARCHAR(50) NOT NULL,  -- Usuario que actualizó el registro
    FOREIGN KEY (usuario_id) REFERENCES users(user_id)  -- Corregido el nombre de la tabla
);

-- Creación de la tabla AnalisisVideo
CREATE TABLE AnalisisVideo (
    id_analisis SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    actividades_id INTEGER NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    nombre_video VARCHAR(255) NOT NULL,
    fecha_analisis TIMESTAMP NOT NULL,
    resultados JSONB NOT NULL,
    created_by VARCHAR(50) NOT NULL,  -- Usuario que creó el registro
    updated_by VARCHAR(50) NOT NULL,  -- Usuario que actualizó el registro
    FOREIGN KEY (usuario_id) REFERENCES users(user_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleado(empleado_id),
    FOREIGN KEY (actividades_id) REFERENCES Actividades(id_actividad)
);