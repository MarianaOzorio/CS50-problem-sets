SELECT title
FROM movies
JOIN stars
ON movies.id = stars.movie_id
JOIN people
ON stars.person_id = people.id
WHERE name = "Helena Bonham Carter"
AND movie_id IN(SELECT movie_id FROM people JOIN stars ON people.id = stars.person_id WHERE name = "Johnny Depp")
