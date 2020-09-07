import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def get_rules():
  with open('app/static/countries.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    rules = []
    for row in data:
      if not first_line:
        rules.append({
          "name": str(row[0]).replace(" ", ""),
          "country": row[0],
          "flight": row[1],
          "quarantine": row[2],
          "additions": row[3]
        })
      else:
        first_line = False
  return rules


@app.route("/")
def index():
  rules = get_rules()
  return render_template("index.html", rules=rules, response='', description='')

@app.route("/submit", methods=["GET", "POST"])
def submit():
  rules = get_rules()

  if request.method == "GET":
    return redirect(url_for('index'))

  elif request.method == "POST":
    country = request.form.get('country_to')
    for rule in rules:
      if rule['name'] == country:
        country = rule['country']
        if rule['quarantine'] == '0':
          quarantine = 'You do not have to be in quarantine once you arrive.'
        else:
          quarantine = 'Once you arrive, you need to be in quarantine for: ' +  rule['quarantine']

        if rule['flight'].strip().lower() == 'yes':
          flight = 'You can travel there. ' + rule['additions'] + "."
        else:
          flight = 'No, you are not allowed to travel there.'
          quarantine = ''

        response = {
          "country": country,
          "flight": flight,
          "quarantine": quarantine
        }
        break   
    
  return render_template("restrictions.html", response=response)

