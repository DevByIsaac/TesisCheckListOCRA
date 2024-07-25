CREATE OR REPLACE PROCEDURE public.create_empleado(
    IN p_rol VARCHAR,
    IN p_nombre VARCHAR,
    IN p_apellido VARCHAR,
    IN p_sexo VARCHAR,
    IN p_edad INTEGER,
    IN p_puesto VARCHAR,
    IN p_estatura FLOAT,
    IN p_horas_trabajo TIME,
    IN p_horas_descanso TIME,
    IN p_created_by VARCHAR,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    INSERT INTO Empleado (rol, Nombre, Apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, created_by, updated_by)
    VALUES (p_rol, p_nombre, p_apellido, p_sexo, p_edad, p_puesto, p_estatura, p_horas_trabajo, p_horas_descanso, p_created_by, p_updated_by);
END;
$$;

CREATE OR REPLACE PROCEDURE public.update_empleado(
    IN p_empleado_id INTEGER,
    IN p_rol VARCHAR,
    IN p_nombre VARCHAR,
    IN p_apellido VARCHAR,
    IN p_sexo VARCHAR,
    IN p_edad INTEGER,
    IN p_puesto VARCHAR,
    IN p_estatura FLOAT,
    IN p_horas_trabajo TIME,
    IN p_horas_descanso TIME,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE Empleado
    SET rol = p_rol,
        Nombre = p_nombre,
        Apellido = p_apellido,
        sexo = p_sexo,
        edad = p_edad,
        puesto = p_puesto,
        estatura = p_estatura,
        horas_trabajo = p_horas_trabajo,
        horas_descanso = p_horas_descanso,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE empleado_id = p_empleado_id;
END;
$$;

CREATE OR REPLACE PROCEDURE public.delete_empleado(
    IN p_empleado_id INTEGER,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    -- Aquí no se elimina físicamente, solo se marca como inactivo
    UPDATE Empleado
    SET state = 'I',
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE empleado_id = p_empleado_id;
END;
$$;

