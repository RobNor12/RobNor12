SELECT name
FROM people
WHERE id IN (
    -- Find the person_id of everyone (stars) who was in those movies
    SELECT person_id
    FROM stars
    WHERE movie_id IN (
        -- Find the movie_id of all movies Kevin Bacon starred in
        SELECT movie_id
        FROM stars
        WHERE person_id = (
            -- Find the ID for the correct Kevin Bacon (born 1958)
            SELECT id
            FROM people
            WHERE name = 'Kevin Bacon' AND birth = 1958
        )
    )
)
AND name != 'Kevin Bacon';
