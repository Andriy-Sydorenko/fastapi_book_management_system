CREATE OR REPLACE FUNCTION create_book_function(
    p_title TEXT,
    p_isbn TEXT,
    p_published_year INT,
    p_genre TEXT,
    p_author_name TEXT
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
    v_author_id INT;
    v_new_book_id INT;
    v_query TEXT;
BEGIN
    v_query := format('SELECT id FROM authors WHERE name ILIKE %L', p_author_name);
    EXECUTE v_query INTO v_author_id;

    IF v_author_id IS NULL THEN
        RAISE EXCEPTION 'Author "%" does not exist', p_author_name;
    END IF;

    v_query := format(
        'INSERT INTO books (title, isbn, published_year, genre, author_id) VALUES (%L, %L, %s, %L, %L) RETURNING id',
        p_title, p_isbn, p_published_year, p_genre, v_author_id
    );
    EXECUTE v_query INTO v_new_book_id;

    v_query := format(
        'SELECT b.id, b.title, b.isbn, b.published_year, b.genre, b.author_id, a.name AS author_name ' ||
        'FROM books b JOIN authors a ON b.author_id = a.id WHERE b.id = %L',
        v_new_book_id
    );
    RETURN QUERY EXECUTE v_query;
END;
$$ LANGUAGE plpgsql;
