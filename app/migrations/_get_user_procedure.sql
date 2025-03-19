CREATE OR REPLACE FUNCTION get_user_by_email_function(p_email TEXT)
RETURNS TABLE(
    id INT,
    email VARCHAR(255),
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE,
    hashed_password VARCHAR(255)
) AS $$
BEGIN
    RETURN QUERY SELECT users.id, users.email, users.full_name, users.created_at, users.hashed_password
    FROM users
    WHERE users.email = p_email;
END;
$$ LANGUAGE plpgsql;