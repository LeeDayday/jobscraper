from flask import Flask, render_template, request, redirect, send_file
from scrap import get_jobs
from exporter import save_to_file
app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = (request.args.get('word'))

  if word:
    word = word.lower()
    existingJobs = db.get(word)
    #검색한 내용이 db에 있는지 탐색
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else:
     return redirect("/")
    #입력한 것이 없다면 home으로 다시
  return render_template("report.html", resultsNumber = len(jobs), searchingBy = word, jobs = jobs)


@app.route("/export")
def export():  
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")

  except:
    return redirect("/")
  word = request.args.get('word')

app.run(host="0.0.0.0")
#repl.it에서 만들어지는 웹사이트 생성

