CREATE OR REPLACE FUNCTION delete_book_function(
    p_book_id INT
)
RETURNS BOOLEAN AS $$
DECLARE
    rows_affected INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM books WHERE id = p_book_id) THEN
        RAISE EXCEPTION 'Book with ID % does not exist', p_book_id;
    END IF;

    DELETE FROM books WHERE id = p_book_id;

    GET DIAGNOSTICS rows_affected = ROW_COUNT;

    RETURN rows_affected > 0;
END;
$$ LANGUAGE plpgsql;
