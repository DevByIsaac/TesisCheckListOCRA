-- Crear o reemplazar el procedimiento create_actividad
CREATE OR REPLACE PROCEDURE public.create_actividad(
    IN p_usuario_id INT,
    IN p_tipo_actividad VARCHAR,
    IN p_descripcion VARCHAR,
    IN p_actividad_repetitiva BOOLEAN,
    IN p_num_pausas INT,
    IN p_lunch_break_duration INT,
    IN p_puntaje_ATD INT,
    IN p_puntaje_ATE FLOAT,
    IN p_puntaje_acciones_fuerza INT,
    IN p_puntaje_FSO INT,
    IN p_puntaje_FFM INT,
    IN p_created_by VARCHAR,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    INSERT INTO Actividades (usuario_id, tipo_actividad, descripcion, actividad_repetitiva, num_pausas,
                              lunch_break_duration, puntaje_ATD, puntaje_ATE, puntaje_acciones_fuerza,
                              puntaje_FSO, puntaje_FFM, created_by, updated_by)
    VALUES (p_usuario_id, p_tipo_actividad, p_descripcion, p_actividad_repetitiva, p_num_pausas,
            p_lunch_break_duration, p_puntaje_ATD, p_puntaje_ATE, p_puntaje_acciones_fuerza,
            p_puntaje_FSO, p_puntaje_FFM, p_created_by, p_updated_by);
END;
$$;

-- Crear o reemplazar el procedimiento update_actividad
CREATE OR REPLACE PROCEDURE public.update_actividad(
    IN p_id_actividad INT,
    IN p_tipo_actividad VARCHAR,
    IN p_descripcion VARCHAR,
    IN p_actividad_repetitiva BOOLEAN,
    IN p_num_pausas INT,
    IN p_lunch_break_duration INT,
    IN p_puntaje_ATD INT,
    IN p_puntaje_ATE FLOAT,
    IN p_puntaje_acciones_fuerza INT,
    IN p_puntaje_FSO INT,
    IN p_puntaje_FFM INT,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE Actividades
    SET tipo_actividad = p_tipo_actividad,
        descripcion = p_descripcion,
        actividad_repetitiva = p_actividad_repetitiva,
        num_pausas = p_num_pausas,
        lunch_break_duration = p_lunch_break_duration,
        puntaje_ATD = p_puntaje_ATD,
        puntaje_ATE = p_puntaje_ATE,
        puntaje_acciones_fuerza = p_puntaje_acciones_fuerza,
        puntaje_FSO = p_puntaje_FSO,
        puntaje_FFM = p_puntaje_FFM,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE id_actividad = p_id_actividad;
END;
$$;

-- Crear o reemplazar el procedimiento delete_actividad
CREATE OR REPLACE PROCEDURE public.delete_actividad(
    IN p_id_actividad INT,
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
