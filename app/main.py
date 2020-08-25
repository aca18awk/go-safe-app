import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def get_rules():
  with open('static/restriction.csv') as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    rules = []
    for row in data:
      if not first_line:
        rules.append({
          "country": row[0],
          "risk": row[1],
          "flight": row[2],
          "quarantine": row[3]
        })
      else:
        first_line = False
  return rules

def get_description():
  description = {
  "country": 'Country: ',
  "risk": 'Risk of getting infected: ',
  "flight": 'Can you travel there: ',
  "quarantine": 'Do you have to be in quarantine once you arrive: '
  }
  return description

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
      if rule['country'] == country:
        response = {
          "country": country,
          "risk": rule['risk'],
          "flight": rule['flight'],
          "quarantine": rule['quarantine']
        }
        break 
      
    description = get_description()       
  return render_template("index.html", rules=rules, response=response, description=description)

