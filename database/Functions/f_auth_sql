CREATE OR REPLACE FUNCTION public.authenticate_user(email TEXT, password TEXT)
RETURNS TABLE(result TEXT) AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM users
        WHERE email = authenticate_user.email
        AND password = authenticate_user.password
    ) THEN
        result := 'success';
    ELSE
        result := 'failure';
    END IF;
END;
$$ LANGUAGE plpgsql;
