CREATE OR REPLACE FUNCTION delete_book_function(
    p_book_id INT
)
RETURNS BOOLEAN AS $$
DECLARE
    rows_affected INT;
BEGIN
    -- Check if the book exists
    IF NOT EXISTS (SELECT 1 FROM books WHERE id = p_book_id) THEN
        RAISE EXCEPTION 'Book with ID % does not exist', p_book_id;
    END IF;

    -- Delete the book
    DELETE FROM books WHERE id = p_book_id;

    -- Get number of rows affected
    GET DIAGNOSTICS rows_affected = ROW_COUNT;

    -- Return true if a book was deleted, false otherwise
    RETURN rows_affected > 0;
END;
$$ LANGUAGE plpgsql;
