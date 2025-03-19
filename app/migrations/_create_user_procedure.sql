CREATE OR REPLACE FUNCTION create_user_function(
    p_email TEXT,
    p_hashed_password TEXT,
    p_full_name TEXT
)
RETURNS TABLE(
    id INT,
    email VARCHAR(255),
    hashed_password VARCHAR(255),
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
    inserted_user RECORD;
BEGIN
    IF p_email IS NULL OR p_email = '' THEN
        RAISE EXCEPTION 'Email cannot be empty';
    END IF;
    IF p_hashed_password IS NULL OR p_hashed_password = '' THEN
        RAISE EXCEPTION 'Password cannot be empty';
    END IF;

    INSERT INTO users (email, hashed_password, full_name)
    VALUES (p_email, p_hashed_password, p_full_name)
    RETURNING * INTO inserted_user;

    -- Use the record directly rather than querying again
    RETURN QUERY
    SELECT
        inserted_user.id,
        inserted_user.email,
        inserted_user.hashed_password,
        inserted_user.full_name,
        inserted_user.created_at;
END;
$$ LANGUAGE plpgsql;
