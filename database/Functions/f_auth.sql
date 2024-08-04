CREATE OR REPLACE FUNCTION public.authenticate_user(
    p_email VARCHAR,
    p_password VARCHAR
)
RETURNS TABLE(auth_result TEXT) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN EXISTS (
                SELECT 1
                FROM users
                WHERE email = p_email
                AND password = crypt(p_password, password)
            ) THEN 'success'
            ELSE 'failure'
        END;
END;
$$;
