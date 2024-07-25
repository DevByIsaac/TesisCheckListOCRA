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
    estatura FLOAT,
    horas_trabajo TIME,
    horas_descanso TIME,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, created_by, updated_by
    FROM Empleado
    WHERE empleado_id = p_empleado_id;
END;
$$;

CREATE OR REPLACE FUNCTION public.get_all_empleados()
RETURNS TABLE(
    empleado_id INTEGER,
    rol VARCHAR,
    Nombre VARCHAR,
    Apellido VARCHAR,
    sexo VARCHAR,
    edad INTEGER,
    puesto VARCHAR,
    estatura FLOAT,
    horas_trabajo TIME,
    horas_descanso TIME,
    created_by VARCHAR,
    updated_by VARCHAR)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT empleado_id, rol, Nombre, Apellido, sexo, edad, puesto, estatura, horas_trabajo, horas_descanso, created_by, updated_by
    FROM Empleado;
END;
$$;
