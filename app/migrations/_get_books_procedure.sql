CREATE OR REPLACE FUNCTION get_books_function(
    p_id INT DEFAULT NULL,
    p_title TEXT DEFAULT NULL,
    p_author TEXT DEFAULT NULL,
    p_genre TEXT DEFAULT NULL,
    p_year_from INT DEFAULT NULL,
    p_year_to INT DEFAULT NULL,
    p_sort_by TEXT DEFAULT 'title',
    p_sort_order TEXT DEFAULT 'asc',
    p_limit INT DEFAULT 10,
    p_offset INT DEFAULT 0
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
    base_query TEXT := 'SELECT b.id, b.title, b.isbn, b.published_year, b.genre, b.author_id, a.name AS author_name FROM books b JOIN authors a ON b.author_id = a.id';
    conditions TEXT := '';
    query TEXT;
BEGIN
    IF p_id IS NOT NULL THEN
        conditions := conditions || format('b.id = %L', p_id) || ' AND ';
    END IF;
    IF p_title IS NOT NULL THEN
        conditions := conditions || format('b.title ILIKE %L', '%' || p_title || '%') || ' AND ';
    END IF;
    IF p_author IS NOT NULL THEN
        conditions := conditions || format('a.name ILIKE %L', '%' || p_author || '%') || ' AND ';
    END IF;
    IF p_genre IS NOT NULL THEN
        conditions := conditions || format('b.genre = %L', p_genre) || ' AND ';
    END IF;
    IF p_year_from IS NOT NULL THEN
        conditions := conditions || format('b.published_year >= %s', p_year_from) || ' AND ';
    END IF;
    IF p_year_to IS NOT NULL THEN
        conditions := conditions || format('b.published_year <= %s', p_year_to) || ' AND ';
    END IF;

    IF conditions <> '' THEN
        conditions := ' WHERE ' || left(conditions, length(conditions) - 5);
    END IF;

    query := base_query || conditions;

    -- Validate sorting parameters against a whitelist.
    IF p_sort_by NOT IN ('title', 'published_year', 'genre', 'isbn') THEN
        p_sort_by := 'title';
    END IF;
    IF lower(p_sort_order) NOT IN ('asc', 'desc') THEN
        p_sort_order := 'asc';
    END IF;

    -- Append ORDER BY, LIMIT, and OFFSET to the query.
    query := query || format(' ORDER BY b.%I %s', p_sort_by, p_sort_order);
    query := query || format(' LIMIT %s OFFSET %s', p_limit, p_offset);

    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;
