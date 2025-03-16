CREATE OR REPLACE FUNCTION delete_author_function(
    p_author_id INT
)
RETURNS VOID AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM authors WHERE id = p_author_id) THEN
        RAISE EXCEPTION 'Author with id % does not exist', p_author_id;
    END IF;

    DELETE FROM books
    WHERE author_id = p_author_id;

    DELETE FROM authors
    WHERE id = p_author_id;

    RAISE NOTICE 'Author with id % and associated books have been deleted.', p_author_id;
END;
$$ LANGUAGE plpgsql;
