CREATE OR REPLACE FUNCTION get_books(
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
    id UUID,
    title TEXT,
    isbn TEXT,
    published_year INT,
    genre TEXT,
    author_id UUID,
    author_name TEXT
) AS $$
DECLARE
    base_query TEXT := 'SELECT b.id, b.title, b.isbn, b.published_year, b.genre, b.author_id, a.name AS author_name FROM books b JOIN authors a ON b.author_id = a.id';
    conditions TEXT := '';
    query TEXT;
BEGIN
    -- Build filtering conditions using safe formatting.
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

    -- If any condition was added, remove the trailing ' AND ' and prepend "WHERE"
    IF conditions <> '' THEN
        conditions := ' WHERE ' || left(conditions, length(conditions) - 5);
    END IF;

    -- Combine base query with filtering conditions.
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

    -- Execute the dynamic SQL and return the resulting rows.
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;
