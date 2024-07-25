CREATE OR REPLACE PROCEDURE create_user(
    p_username VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_created_by VARCHAR,
    p_updated_by VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO users (username, email, password, state, created_by, updated_by)
    VALUES (p_username, p_email, crypt(p_password, gen_salt('bf')), 'A', p_created_by, p_updated_by);
END;
$$;

CREATE OR REPLACE PROCEDURE update_user(
    p_user_id INT,
    p_username VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_state VARCHAR,
    p_updated_by VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET 
        username = p_username,
        email = p_email,
        password = crypt(p_password, gen_salt('bf')),
        state = p_state,
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE user_id = p_user_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user(p_user_id INT, p_updated_by VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET 
        state = 'I',
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_updated_by
    WHERE user_id = p_user_id;
END;
$$;
