create view my_view as 
select film.film_id
    , film.release_date
    , genres.genre
    , production_company.company_name
    from film join film_genres on film.film_id = film_genres.film_film_id
        join genres on film_genres.genres_genre_id = genres.genre_id
        join film_company on film.film_id = film_company.film_film_id
        join production_company on film_company.production_company_id = production_company.company_id;