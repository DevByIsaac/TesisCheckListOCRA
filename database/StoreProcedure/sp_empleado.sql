CREATE OR REPLACE PROCEDURE public.create_empleado(
    IN p_rol VARCHAR,
    IN p_nombre VARCHAR,
    IN p_apellido VARCHAR,
    IN p_sexo VARCHAR,
    IN p_edad INTEGER,
    IN p_puesto VARCHAR,
    IN p_duracion_turno INTEGER,
    IN p_duracion_descanso INTEGER,
    IN p_duracion_tiempo_libre INTEGER,
    IN p_created_by VARCHAR,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    INSERT INTO Empleado (rol, Nombre, Apellido, sexo, edad, puesto, duracion_turno, duracion_descanso, duracion_tiempo_libre, created_by, updated_by)
    VALUES (p_rol, p_nombre, p_apellido, p_sexo, p_edad, p_puesto, p_duracion_turno, p_duracion_descanso, p_duracion_tiempo_libre, p_created_by, p_updated_by);
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
    IN p_duracion_turno INTEGER,
    IN p_duracion_descanso INTEGER,
    IN p_duracion_tiempo_libre INTEGER,
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
        duracion_turno = p_duracion_turno,
        duracion_descanso = p_duracion_descanso,
        duracion_tiempo_libre = p_duracion_tiempo_libre,
        updated_at = CURRENT_INTEGERSTAMP,
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
    SET state = 'I',  -- Asumiendo que `state` es un campo que indica el estado de inactividad
        updated_at = CURRENT_INTEGERSTAMP,
        updated_by = p_updated_by
    WHERE empleado_id = p_empleado_id;
END;
$$;


