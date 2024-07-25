CREATE OR REPLACE FUNCTION public.get_analisis_video_by_id(
    p_id_analisis INTEGER)
RETURNS TABLE(
    id_analisis INTEGER,
    usuario_id INTEGER,
    empleado_id INTEGER,
    actividades_id INTEGER,
    modelo VARCHAR,
    nombre_video VARCHAR,
    fecha_analisis TIMESTAMP,
    resultados JSONB,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT id_analisis, usuario_id, empleado_id, actividades_id, modelo, nombre_video, fecha_analisis, resultados, created_by, updated_by
    FROM AnalisisVideo
    WHERE id_analisis = p_id_analisis;
END;
$$;
