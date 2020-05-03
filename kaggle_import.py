import cx_Oracle

import csv

connection = cx_Oracle.connect("LAB_3/Optiquest22@localhost:1521/xe", encoding="UTF-8", nencoding="UTF-8")

def get_str(a):
    mystring = str(a)
    mystring = mystring.replace("'", "")
    mystring = mystring.replace("&", " and ")
    mystring = mystring.replace(";", ",")
    if mystring == "":
        mystring = "0"
    return mystring

country_list1 = []
country_list2 = set()
data = []
with open('country_csv.csv', newline='', encoding='utf-8') as csvfile:
    myline = csvfile.readline()
    myreader = csv.reader(csvfile)
    for row in myreader:
        data.append((get_str(row[1]), get_str(row[0])))


query = """insert into production_country(country_id, country_name) values (:country_id, :country_name)"""

cursor = connection.cursor()

for el in data:
    print(el[0]+" "+el[1])
    cursor.execute(query, country_id=el[0], country_name=el[1])
    country_list1.append(el[0])
cursor.execute(query, country_id='0', country_name='Not mentioned')

country_list1.append('0')
cursor.close()
connection.commit()

data = []
with open('language-codes_csv.csv', newline='', encoding='utf-8') as csvfile:
    myline = csvfile.readline()
    myreader = csv.reader(csvfile)
    for row in myreader:
        data.append((get_str(row[0]), get_str(row[1])))

query = """insert into spoken_language(language_id, language_name) values (:language_id, :language_name)"""

cursor = connection.cursor()

cursor.prepare(query)

cursor.executemany(None, data)

cursor.close()
connection.commit()

film_country = []
film_language = []
film_genres = []
film_company = []
films = []
genres_dict = dict()
companies = dict()

with open('tmdb_5000_movies.csv', newline='', encoding='utf-8') as csvfile:
    myline = csvfile.readline()
    spamreader = csv.reader(csvfile)
    for row in spamreader:
         #file.write("""INSERT INTO FILM (FILM_ID, BUDGET, HOMEPAGE, ORIGINAL_TITLE,
         #      RELEASE_DATE, RUNTIME) VALUES ();\n""")
         films.append((get_str(row[3]), get_str(row[0]), get_str(row[2]), get_str(row[6]), get_str(row[11]), get_str(row[13])))
         if row[1] ==[]:
             row[1] = """[{""id"": 0, ""name"": ""Not mentioned""}]"""
         row[1] = row[1][1:-1]
         new_list = row[1][:-1].split("}, ")
         new_list3 = list()
         new_list4 = list()
         for el in new_list:
             el = el[1:]
             new_list2 = el.split(", ")
             new_list3.append(new_list2[0].split(": ")[1])
             new_list4.append(new_list2[1].split(": ")[1])
         n = len(new_list3)
         i = 0
         while(i<n):
             genres_dict[int(new_list3[i])] = new_list4[i][1:-1]
             film_genres.append((get_str(row[3]), int(new_list3[i])))
             i = i + 1

         if row[9] == "[]":
             row[9] = """[{""Name"":  ""Not mentioned"" , ""id"": 0}]"""
         row[9] = row[9][1:-1]
         new_list = row[9][:-1].split("}, ")
         new_list3 = list()
         new_list4 = list()
         for el in new_list:
             el = el[1:]
             new_list2 = el.split(", \"")
             new_list3.append(new_list2[0].split(": ")[1])
             new_list4.append(new_list2[1].split(": ")[1])
         n = len(new_list3)
         i = 0
         while (i < n):
             companies[int(new_list4[i])] = new_list3[i][1:-1]
             film_company.append((get_str(row[3]), int(new_list4[i])))
             i = i + 1


         if row[10] == "[]":
             row[10] = """[{""id"": "0", ""name"": ""Not mentioned""}]"""
         row[10] = row[10][1:-1]
         new_list = row[10][:-1].split("}, ")
         new_list3 = list()
         new_list4 = list()
         for el in new_list:
             el = el[1:]
             new_list2 = el.split(", ")
             new_list3.append(new_list2[0].split(": ")[1])
             new_list4.append(new_list2[1].split(": ")[1])
             n = len(new_list3)
             i = 0
         while (i < n):
             film_country.append((get_str(row[3]), get_str(new_list3[i][1: -1])))
             i = i+1


         if row[14] == "[]":
             row[14] = """[{""id"": "0", ""name"": ""Not mentioned""}]"""
         row[14] = row[14][1:-1]
         new_list = row[14][:-1].split("}, ")
         new_list3 = list()
         new_list4 = list()
         for el in new_list:
             el = el[1:]
             new_list2 = el.split(", ")
             new_list3.append(new_list2[0].split(": ")[1])
             n = len(new_list3)
             i = 0
         while (i < n):
             film_language.append((new_list3[i][1: -1], get_str(row[3])))
             i = i + 1


query = "insert into film(film_id, budget, homepage, original_title, release_date, runtime) values(:film_id, :budget, :homepage, :original_title, TO_DATE(:release_date, 'yyyy-mm-dd'), :runtime)"

cursor = connection.cursor()
cursor.prepare(query)

cursor.executemany(None, films)

cursor.close()
connection.commit()


query = "insert into genres(genre_id, genre) values(:genre_id, :genre_name)"

cursor = connection.cursor()
cursor.prepare(query)

genres_list = [ el for el in genres_dict.items()]
cursor.executemany(None, genres_list)

cursor.close()
connection.commit()


query = "insert into production_company(company_id, company_name) values(:company_id, :company_name)"

cursor = connection.cursor()
cursor.prepare(query)

companies_list = [ el for el in companies.items()]
cursor.executemany(None, companies_list)

cursor.close()
connection.commit()


query = "insert into film_company(film_film_id, production_company_id) values(:film_id, :company_id)"

cursor = connection.cursor()
cursor.prepare(query)

cursor.executemany(None, film_company)

cursor.close()
connection.commit()


query = "insert into film_genres(film_film_id, genres_genre_id) values(:film_id, :genre_id)"

cursor = connection.cursor()
cursor.prepare(query)

cursor.executemany(None, film_genres)

cursor.close()
connection.commit()



query = "insert into film_country(film_film_id, production_country_id) values(:film_id, :country_id)"

cursor = connection.cursor()
cursor.prepare(query)
print(len(film_country))
cursor.executemany(None, film_country)

cursor.close()
connection.commit()


query = "insert into film_languages(spoken_language_language_id, film_film_id) values(:language_id, :film_id)"

cursor = connection.cursor()
cursor.prepare(query)

cursor.executemany(None, film_language)

cursor.close()
connection.commit()
