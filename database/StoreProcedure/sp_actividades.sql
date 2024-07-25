CREATE OR REPLACE PROCEDURE public.create_actividad(
    IN p_usuario_id INTEGER,
    IN p_tipo_actividad VARCHAR,
    IN p_descripcion VARCHAR,
    IN p_fecha_actividad TIMESTAMP,
    IN p_created_by VARCHAR,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    INSERT INTO Actividades (usuario_id, tipo_actividad, descripcion, fecha_actividad, created_by, updated_by)
    VALUES (p_usuario_id, p_tipo_actividad, p_descripcion, p_fecha_actividad, p_created_by, p_updated_by);
END;
$$;

CREATE OR REPLACE PROCEDURE public.update_actividad(
    IN p_id_actividad INTEGER,
    IN p_tipo_actividad VARCHAR,
    IN p_descripcion VARCHAR,
    IN p_fecha_actividad TIMESTAMP,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE Actividades
    SET tipo_actividad = p_tipo_actividad,
        descripcion = p_descripcion,
        fecha_actividad = p_fecha_actividad,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE id_actividad = p_id_actividad;
END;
$$;

CREATE OR REPLACE PROCEDURE public.delete_actividad(
    IN p_id_actividad INTEGER,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    -- Aquí no se elimina físicamente, solo se marca como inactivo
    UPDATE Actividades
    SET state = 'I',
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE id_actividad = p_id_actividad;
END;
$$;
