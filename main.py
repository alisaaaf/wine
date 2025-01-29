from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas
import pprint
import pandas
import pprint
from collections import defaultdict

data = pandas.read_excel('wine3.xlsx', na_values = ['N/A', 'NA'], keep_default_na=False)
drinks = data.to_dict(orient="records")

grouped_drinks = defaultdict(list)

for drink in drinks:
    grouped_drinks[drink["Категория"]].append(drink)

def get_year_word(year):
    if year % 10 == 1:
        return "год"
    elif 11 <= year % 100 <= 19:
        return "лет"
    elif 2 <= (year % 10) <= 4:
        return "года"
    else:
        return "лет"

years_since_1920 = datetime.date.today().year - 1920
year_word = get_year_word(years_since_1920)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    years_since_1920 = years_since_1920,
    year_word = year_word,
    white_wines = grouped_drinks["Белые вина"],
    red_wines = grouped_drinks["Красные вина"],
    drinks = grouped_drinks["Напитки"]
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

print(1)
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

