# fastapi, uvicorn, requests, beautifulsoup4, re

from fastapi import FastAPI

import re

import os

import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Takes a search query as an input and returns all possible tournaments along with their respective location, date, circuits, and IDs. 
@app.get("/api/search/{query}")
async def search(query: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Cookie': os.environ.get('TABROOM_COOKIE')
    })
    resp = session.get(f"https://www.tabroom.com/index/search.mhtml?search={query}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    
    results = []
    for row in soup.find_all('tr'):
        columns = row.select('td')
        if len(columns) >= 4:
            tournament_name = columns[0].select_one('a.plain').text.strip()
            location = columns[1].get_text(strip=True)
            date = columns[2].get_text(strip=True)
            circuits = columns[3].get_text(strip=True)
            tourn_id = columns[0].select_one('a.plain').get('href')
            tournament = {
                "name": tournament_name,
                "location": location.replace("\n\t\t\t\t\t\t", ""),
                "date": date,
                "circuits": circuits,
                "tourn_id": tourn_id.replace("/index/tourn/index.mhtml?tourn_id=", "")
            }
            results.append(tournament)
    return {"results": results}


# Takes a tournament id as an input and returns all events and their respective IDs at that tournament. 
@app.get("/api/events/{tourn_id}")
async def events(tourn_id: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Cookie': os.environ.get('TABROOM_COOKIE')
    })
    resp = session.get(f"https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    events = []
    for row in soup.find_all("a", class_="blue"):
        event_name = row.get_text(strip=True)
        event_id = row.get("href")
        event = {
            "name": event_name,
            "event_id": event_id.replace(f"/index/tourn/fields.mhtml?tourn_id={tourn_id}&event_id=", "")
        }
        events.append(event)
    return {"events": events}

# Takes a tournament id and event id as inputs and returns all entries. 
@app.get("/api/entries/{tourn_id}/{event_id}")
async def entries(tourn_id: str, event_id: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Cookie': os.environ.get('TABROOM_COOKIE')
    })
    resp = session.get(f"https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}&event_id={event_id}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    entries = []
    table = soup.find("table", {"id": "fieldsort"})
    if table:
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 5: # Debate entries with records
                school = columns[0].get_text(strip=True)
                location = columns[1].get_text(strip=True)
                entry = columns[2].get_text(strip=True)
                code = columns[3].get_text(strip=True)
                record = columns[4].find('a')['href']
                competitor = {
                    "school": school,
                    "location": location,
                    "entry": entry,
                    "code": code,
                    "record": "https://www.tabroom.com"+record
                }
                entries.append(competitor)
            elif len(columns) >= 4: # Speech entries withoutrecords
                school = columns[0].get_text(strip=True)
                location = columns[1].get_text(strip=True)
                entry = columns[2].get_text(strip=True)
                code = columns[3].get_text(strip=True)
                competitor = {
                    "school": school,
                    "location": location,
                    "entry": entry,
                    "code": code,
                }
                entries.append(competitor)
    return {"entries": entries}

# Takes a tournament id and event id as an inputs and returns all of the rounds and their respective IDs. 
@app.get("/api/rounds/{tourn_id}/{event_id}")
async def rounds(tourn_id: str, event_id: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Cookie': os.environ.get('TABROOM_COOKIE'),
        'Referer': 'https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id={tourn_id}&round_id=0',
    })
    payload = {
        'tourn_id': {tourn_id},
        'event_id': {event_id}
    }
    resp = session.post("https://www.tabroom.com/index/tourn/postings/index.mhtml", payload)
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    rounds = []
    side_note_div = soup.find("div", class_="sidenote")
    for group in side_note_div.find_all("a"):
        round_name = group.get_text(strip=True)
        round_id = group.get("href")
        if round_id.find("judge_list") and round_id.find("jpool"):
            event = {
                "round_name": round_name.replace("\n\t\t\t\t\t\t\t\t", " "),
                "round_id": round_id.split("=")[-1]
            }
            rounds.append(event)
    
    return {"rounds": rounds}

# Takes a tournament id and round id as inputs and returns all pairings. 
@app.get("/api/pairings/{tourn_id}/{round_id}")
async def pairings(tourn_id: str, round_id: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Cookie': os.environ.get('TABROOM_COOKIE')
    })
    resp = session.get(f"https://www.tabroom.com/index/tourn/postings/round.mhtml?tourn_id={tourn_id}&round_id={round_id}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    pairings = []
    table = soup.find('table')
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        entry = {}
        for i, column in enumerate(columns):
            header = table.find('thead').find('tr').find_all('th')[i].get_text(strip=True)
            value = re.sub(r"[*|\n|\t]", "", column.get_text(strip=True))
            entry[header] = value
        if entry:
            pairings.append(entry)
    return {"pairings": pairings}
