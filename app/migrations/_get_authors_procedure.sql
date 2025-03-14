CREATE OR REPLACE FUNCTION get_authors_procedure(
    p_id INT DEFAULT NULL,
    p_name TEXT DEFAULT NULL
)
RETURNS TABLE(
    id INT,
    name VARCHAR(255)
) AS $$
DECLARE
    base_query TEXT := 'SELECT id, name FROM authors';
    conditions TEXT := '';
    query TEXT;
BEGIN
    IF p_id IS NOT NULL THEN
        conditions := conditions || format('id = %L', p_id) || ' AND ';
    END IF;
    IF p_name IS NOT NULL THEN
        conditions := conditions || format('name ILIKE %L', p_name) || ' AND ';
    END IF;

    IF conditions <> '' THEN
        conditions := ' WHERE ' || left(conditions, length(conditions) - 5);
    END IF;

    query := base_query || conditions;
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;
