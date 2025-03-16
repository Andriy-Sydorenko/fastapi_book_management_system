CREATE OR REPLACE FUNCTION update_author_function(
    p_author_id INT,
    p_name VARCHAR(255)
)
RETURNS SETOF authors AS $$
BEGIN
    RETURN QUERY
    UPDATE authors
    SET name = p_name
    WHERE id = p_author_id
    RETURNING *;
END;
$$ LANGUAGE plpgsql;
