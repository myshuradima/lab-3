import cx_Oracle
import plotly.offline as py
import plotly.graph_objs as go
connection = cx_Oracle.connect("LAB_3/Optiquest22@localhost:1521/xe")

cursor = connection.cursor()
query = """
select company_name
, count(film_id)
from my_view
group by company_name
order by count(film_id) desc"""


cursor.execute(query)

company = []
films_amount = []

for row in cursor:
    print("Company name: ", row[0], " amount of films: ", row[1])
    if int(row[1]) > 50:
        company += [row[0]]
        films_amount += [row[1]]

data = [go.Bar(
        x=company,
        y=films_amount
)]

layout = go.Layout(
    title='Companies-amount-of-films',
    xaxis=dict(
        title='Companies',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
            title='Amount of films',
            rangemode='nonnegative',
            autorange=True,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
fig1 = go.Figure(data=data, layout=layout)

company_amount_of_films = py.plot(fig1)

cursor = connection.cursor()

query = """
select genre
, count(film_id)
from my_view
group by genre 
order by count(film_id) desc"""


cursor.execute(query)

genre = []
films_amount = []

for row in cursor:
    print("Genre name: ", row[1], " amount of films: ", row[0])
    genre += [row[0]]
    films_amount += [row[1]]

pie = go.Pie(
        labels=genre,
        values=films_amount
)

genres_amount_of_films = py.plot([pie])

cursor = connection.cursor()

cursor.execute("""
select sum(amount)
, 'Summer' as time 
, film_year
from(
    select count(my_view.film_id) as amount 
    ,extract(month from release_date) as film_month
    ,extract(year from release_date) as film_year
    from my_view
    group by extract(year from release_date), extract(month from release_date))
where film_month in ('6', '7', '8')
group by film_year

union

select sum(amount)
, 'Winter' as time
,film_year
from(
select count(my_view.film_id) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from my_view
group by extract(year from release_date), extract(month from release_date))
where film_month in ('12', '1', '2')
group by film_year

union

select sum(amount)
, 'Spring' as time
, film_year
from(
select count(my_view.film_id) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from my_view
group by extract(year from release_date), extract(month from release_date))
where film_month in ('3', '4', '5')
group by film_year

union

select sum(amount)
, 'Autumn' as time
, film_year
from(
select count(my_view.film_id) as amount 
,extract(month from release_date) as film_month
,extract(year from release_date) as film_year
from my_view
group by extract(year from release_date), extract(month from release_date))
where film_month in ('9', '10', '11')
group by film_year
order by film_year
""")
release_dates = []
amount_of_films = []

for row in cursor:
    if row[2] >1990:
        print("Date ", row[1] + str(row[2]), " sum: ", row[0])
        release_dates += [row[1] + str(row[2])]
        amount_of_films += [row[0]]

order_date_prices = go.Scatter(
    x=release_dates,
    y=amount_of_films,
    mode='lines+markers'
)

data = [order_date_prices]
py.plot(data)
