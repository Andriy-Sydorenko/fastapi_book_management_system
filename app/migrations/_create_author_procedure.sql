CREATE OR REPLACE FUNCTION create_author_function(
    p_name TEXT
)
RETURNS TABLE(
    id INT,
    name VARCHAR(255)
) AS $$
DECLARE
    v_author_id INT;
    v_query TEXT;
BEGIN
    -- Check if the author already exists.
    v_query := format('SELECT id FROM authors WHERE name ILIKE %L', p_name);
    EXECUTE v_query INTO v_author_id;

    IF v_author_id IS NOT NULL THEN
        RAISE EXCEPTION 'Author with name "%" already exists.', p_name;
    END IF;

    -- Insert the new author and return the new record.
    v_query := format('INSERT INTO authors (name) VALUES (%L) RETURNING id, name', p_name);
    RETURN QUERY EXECUTE v_query;
END;
$$ LANGUAGE plpgsql;
