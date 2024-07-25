CREATE OR REPLACE PROCEDURE public.create_analisis_video(
    IN p_usuario_id INTEGER,
    IN p_empleado_id INTEGER,
    IN p_actividades_id INTEGER,
    IN p_modelo VARCHAR,
    IN p_nombre_video VARCHAR,
    IN p_fecha_analisis TIMESTAMP,
    IN p_resultados JSONB,
    IN p_created_by VARCHAR,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    INSERT INTO AnalisisVideo (usuario_id, empleado_id, actividades_id, modelo, nombre_video, fecha_analisis, resultados, created_by, updated_by)
    VALUES (p_usuario_id, p_empleado_id, p_actividades_id, p_modelo, p_nombre_video, p_fecha_analisis, p_resultados, p_created_by, p_updated_by);
END;
$$;

CREATE OR REPLACE PROCEDURE public.update_analisis_video(
    IN p_id_analisis INTEGER,
    IN p_usuario_id INTEGER,
    IN p_empleado_id INTEGER,
    IN p_actividades_id INTEGER,
    IN p_modelo VARCHAR,
    IN p_nombre_video VARCHAR,
    IN p_fecha_analisis TIMESTAMP,
    IN p_resultados JSONB,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE AnalisisVideo
    SET usuario_id = p_usuario_id,
        empleado_id = p_empleado_id,
        actividades_id = p_actividades_id,
        modelo = p_modelo,
        nombre_video = p_nombre_video,
        fecha_analisis = p_fecha_analisis,
        resultados = p_resultados,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE id_analisis = p_id_analisis;
END;
$$;

CREATE OR REPLACE PROCEDURE public.delete_analisis_video(
    IN p_id_analisis INTEGER,
    IN p_updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    -- Aquí no se elimina físicamente, solo se marca como inactivo
    UPDATE AnalisisVideo
    SET state = 'I',
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE id_analisis = p_id_analisis;
END;
$$;
