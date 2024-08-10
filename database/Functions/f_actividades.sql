-- Eliminar la función get_empleado_by_id si ya existe
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'get_empleado_by_id' AND pg_function_is_visible(oid)) THEN
        EXECUTE 'DROP FUNCTION public.get_empleado_by_id(INTEGER)';
    END IF;
END
$$;

-- Crear o reemplazar la función get_empleado_by_id
CREATE OR REPLACE FUNCTION public.get_empleado_by_id(
    p_empleado_id INTEGER)
RETURNS TABLE(
    empleado_id INTEGER,
    rol VARCHAR,
    Nombre VARCHAR,
    Apellido VARCHAR,
    sexo VARCHAR,
    edad INTEGER,
    puesto VARCHAR,
    duracion_turno TIME,
    duracion_descanso TIME,
    duracion_tiempo_libre TIME,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto,
           duracion_turno, duracion_descanso, duracion_tiempo_libre,
           created_by, updated_by
    FROM Empleado
    WHERE empleado_id = p_empleado_id;
END;
$$;

-- Eliminar la función get_all_empleados si ya existe
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'get_all_empleados' AND pg_function_is_visible(oid)) THEN
        EXECUTE 'DROP FUNCTION public.get_all_empleados()';
    END IF;
END
$$;

-- Crear o reemplazar la función get_all_empleados
CREATE OR REPLACE FUNCTION public.get_all_empleados()
RETURNS TABLE(
    empleado_id INTEGER,
    rol VARCHAR,
    Nombre VARCHAR,
    Apellido VARCHAR,
    sexo VARCHAR,
    edad INTEGER,
    puesto VARCHAR,
    duracion_turno TIME,
    duracion_descanso TIME,
    duracion_tiempo_libre TIME,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto,
           duracion_turno, duracion_descanso, duracion_tiempo_libre,
           created_by, updated_by
    FROM Empleado;
END;
$$;
