CREATE OR REPLACE FUNCTION update_book_function(
    p_book_id INT,
    p_title TEXT DEFAULT NULL,
    p_isbn TEXT DEFAULT NULL,
    p_published_year INT DEFAULT NULL,
    p_genre TEXT DEFAULT NULL,
    p_author_name TEXT DEFAULT NULL
)
RETURNS TABLE(
    id INT,
    title VARCHAR(255),
    isbn VARCHAR(13),
    published_year INT,
    genre VARCHAR(50),
    author_id INT,
    author_name VARCHAR(255)
) AS $$
DECLARE
    v_update_parts TEXT := '';
    v_author_id INT;
    v_query TEXT;
BEGIN
    -- Check if the book exists - explicitly reference books.id
    IF NOT EXISTS (SELECT 1 FROM books WHERE books.id = p_book_id) THEN
        RAISE EXCEPTION 'Book with ID % does not exist', p_book_id;
    END IF;

    -- Check if author exists and get author_id if author_name is provided
    IF p_author_name IS NOT NULL THEN
        v_query := format('SELECT authors.id FROM authors WHERE authors.name ILIKE %L', p_author_name);
        EXECUTE v_query INTO v_author_id;

        IF v_author_id IS NULL THEN
            RAISE EXCEPTION 'Author "%" does not exist', p_author_name;
        END IF;
    END IF;

    -- Build update query dynamically based on provided parameters
    IF p_title IS NOT NULL THEN
        v_update_parts := v_update_parts || format('title = %L', p_title) || ', ';
    END IF;

    IF p_isbn IS NOT NULL THEN
        v_update_parts := v_update_parts || format('isbn = %L', p_isbn) || ', ';
    END IF;

    IF p_published_year IS NOT NULL THEN
        v_update_parts := v_update_parts || format('published_year = %s', p_published_year) || ', ';
    END IF;

    IF p_genre IS NOT NULL THEN
        v_update_parts := v_update_parts || format('genre = %L', p_genre) || ', ';
    END IF;

    IF v_author_id IS NOT NULL THEN
        v_update_parts := v_update_parts || format('author_id = %s', v_author_id) || ', ';
    END IF;

    -- Check if any updates were specified
    IF v_update_parts = '' THEN
        RAISE EXCEPTION 'No update parameters provided';
    END IF;

    -- Remove trailing comma and space
    v_update_parts := LEFT(v_update_parts, LENGTH(v_update_parts) - 2);

    -- Perform the update - explicitly reference books.id
    v_query := format(
        'UPDATE books SET %s WHERE books.id = %s',
        v_update_parts, p_book_id
    );
    EXECUTE v_query;

    -- Return the updated book record - explicitly qualify ALL column references
    RETURN QUERY
    SELECT
        b.id,
        b.title,
        b.isbn,
        b.published_year,
        b.genre,
        b.author_id,
        a.name AS author_name
    FROM books b
    JOIN authors a ON b.author_id = a.id
    WHERE b.id = p_book_id;
END;
$$ LANGUAGE plpgsql;
