import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text().strip()
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find("h3", {
        "class": "mb4"
    }).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip(" \r")
    job_id = html['data-jobid']
    return {"title": title, "company": company, "location": location,
    "link":f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"scrapping SO Page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def extract_wework(word):
  jobs = []
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  result=requests.get(url)
  soup = BeautifulSoup(result.text,"html.parser")
  lists = soup.find("section",{"class":"jobs"}).find("ul").find_all(
    "li",{"class":"feature"}
  )

  for list in lists:


    job_link = list.find_all("a")

    if len(job_link) > 1:
            job_link = job_link[1]
    else:
            job_link = job_link[0]
#link 개수가 2 이하이면 홈페이지의 첫번째 li class가 공백임
    job_info = job_link.find_all("span")

    company = job_info[0].get_text()
    title = job_info[1].get_text()
    location = job_info[5].get_text()
    link = f"https://weworkremotely.com{job_link['href']}"

    job = {"title": title,
    "company": company,
    "location": location,
    "link": link
        }
    jobs.append(job)

  return jobs
    
def extract_remoteok(word):
  jobs = []
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  result = requests.get(url)
  soup = BeautifulSoup(result.text,"html.parser")
  trs = soup.find_all("tr",{"class":"job"})

  for tr in trs:
    tds = tr.find_all("td")
    link = tds[0].find("a")['href']
    if not link:
      link = ""
    link = f"https://remoteok.com/{link['href']}"
    title = tds[1].find("h2")
    if title:
      title = title.text
    else:
      title = ""
    company = tds[1].find("a").find("h2")
    if company:
      company = company.text
    else:
      company = ""
    location = tds[1].find("a").find("div",{"class":"location"})
    if location:
      location = location.text
    else:
      location=""
    
    job = {
      "title":title, "company":company, "location":location, "link":link
    }
    jobs.append(job)
  return jobs
  
def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
  
  last_page = get_last_page(url)
  so_jobs = extract_jobs(last_page,url)
  wework_jobs = extract_wework(word)
  remoteok_jobs = extract_remoteok(word)
  jobs = so_jobs + wework_jobs + remoteok_jobs
  return jobs
