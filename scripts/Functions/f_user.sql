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