CREATE OR REPLACE FUNCTION get_user_by_id(p_user_id INT)
RETURNS TABLE (
    user_id INT,
    username VARCHAR,
    email VARCHAR,
    state VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    created_by VARCHAR,
    updated_by VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT user_id, username, email, state, created_at, updated_at, created_by, updated_by
    FROM users
    WHERE user_id = p_user_id;
END;
$$;

-- FUNCTION: public.get_all_users()

-- DROP FUNCTION IF EXISTS public.get_all_users();

CREATE OR REPLACE FUNCTION public.get_all_users()
RETURNS TABLE(
    user_id integer,
    username character varying,
    email character varying,
    state character varying,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    created_by character varying,
    updated_by character varying
) 
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY
    SELECT u.user_id, u.username, u.email, u.state, u.created_at, u.updated_at, u.created_by, u.updated_by
    FROM users u
    WHERE u.state = 'A';
END;
$$;

