CREATE OR REPLACE FUNCTION public.get_actividad_by_id(
    p_id_actividad INTEGER)
RETURNS TABLE(
    id_actividad INTEGER,
    usuario_id INTEGER,
    tipo_actividad VARCHAR,
    descripcion VARCHAR,
    fecha_actividad TIMESTAMP,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT id_actividad, usuario_id, tipo_actividad, descripcion, fecha_actividad, created_by, updated_by
    FROM Actividades
    WHERE id_actividad = p_id_actividad;
END;
$$;
