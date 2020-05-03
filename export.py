import csv
import cx_Oracle

connection = cx_Oracle.connect("LAB_3/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

cursor_film = connection.cursor()

cursor_film.execute(
"""select trim(film_id) as film_id
, trim(budget) as budget
, trim(homepage) as homepage
, trim(release_date) as release_date
, trim(runtime) as runtime
from film""")

with open("my_films.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for film_id, budget, homepage, release_date, runtime in cursor_film:
        cursor_genre = connection.cursor()
        query = """select trim(genre_id) as genre_id
                , trim(genre)  as genre
                from film_genres join genres on genres.genre_id = film_genres.genres_genre_id
                where film_genres.film_film_id = :film_id"""
        cursor_genre.execute(query, film_id=film_id)
        genres = "["
        for genre_id, genre in cursor_genre:
            genres = genres + "{id:" + genre_id + ", genre:" + genre + "},"
        genres = genres[0:-1] + "]"
        cursor_genre.close()

        cursor_company = connection.cursor()
        query = """select trim(company_id) as company_id
                        , trim(company_name)  as company_name
                        from film_company join production_company on production_company.company_id = film_company.production_company_id
                        where film_company.film_film_id = :film_id"""
        cursor_company.execute(query, film_id=film_id)
        companies = "["
        for company_id, company_name in cursor_company:
            companies = companies + "{id:" + company_id + ", name:" + company_name + "},"
        companies = companies[0:-1] + "]"
        cursor_company.close()

        cursor_country = connection.cursor()
        query = """select trim(country_id) as country_id
                               , trim(country_name)  as country_name
                               from film_country join production_country on production_country.country_id = film_country.production_country_id
                               where film_country.film_film_id = :film_id"""
        cursor_country.execute(query, film_id=film_id)
        countries = "["
        for country_id, country_name in cursor_country:
            countries = countries + "{id:" + country_id + ", name:" + country_name + "},"
        countries = countries[0:-1] + "]"
        cursor_country.close()

        cursor_languages = connection.cursor()
        query = """select trim(language_id) as language_id
                                       , trim(language_name)  as language_name
                                       from film_languages join spoken_language on film_languages.spoken_language_language_id = 
                                       spoken_language.language_id
                                       where film_languages.film_film_id = :film_id"""
        cursor_languages.execute(query, film_id=film_id)
        languages = "["
        for language_id, language_name in cursor_languages:
            languages = languages + "{id:" + language_id + ", name:" + language_name + "},"
        languages = languages[0:-1] + "]"
        cursor_languages.close()

        writer.writerow([film_id, budget, homepage, release_date, runtime, genres, companies, countries, languages])



cursor_film.close()
