# vercel-tabroom-info-api
An unofficial API created to query information such as tournaments, events, entries, rounds, and pairings. This is the vercel repository for python runtime with serverless functions. This is modified to be easily uploaded to a Vercel instance. 

# Setup
## Import from GitHub
  Import the Git repository to a new project on Vercel. 
## Environment Variables
Setup environment variables to store the cookie, username, and password. Replace the username and password below with the respective account that you want to use. 
> :warning: **These variables are stored as environment variables:** Implement encryption (Vercel should auto-encrypt these) if you want them to be secure!
```
TABROOM_COOKIE=" "
USERNAME="username"
PASSWORD="password"
```

# Usage
All of the following are GET Requests. 
## /api/search/{query}
Takes a search query as an input and returns all possible tournaments along with their respective location, date, circuits, and IDs.
### Example
```
http://127.0.0.1:8000/api/search/Wyoming+State
```
```
{
  "results": [
    {
      "name": "Wyoming State Speech Debate",
      "location": "Cheyenne, WY/US",
      "date": "2023-03-09",
      "circuits": "WY",
      "tourn_id": "26753"
    },
    {
      "name": "Wyoming State Speech and Debate",
      "location": "Riverton, WY/US",
      "date": "2022-03-10",
      "circuits": "WY",
      "tourn_id": "23017"
    }
  ]
}
```
## /api/events/{tourn_id}
Takes a tournament id as an input and returns all events and their respective IDs at that tournament. 
### Example
```
http://127.0.0.1:8000/api/events/26155
```
```
{
  "events": [
    {
      "name": "Congress",
      "event_id": "237908"
    },
    {
      "name": "LD Debate",
      "event_id": "237916"
    },
    {
      "name": "Policy Debate",
      "event_id": "237921"
    },
    {
      "name": "PF Debate",
      "event_id": "237919"
    },
    {
      "name": "Big Questions",
      "event_id": "237907"
    },
    {
      "name": "Duet Acting",
      "event_id": "237910"
    },
    {
      "name": "Original Spoken Word Poetry",
      "event_id": "237918"
    },
    {
      "name": "Extemporaneous Speaking",
      "event_id": "237912"
    },
    ...
  ]
}
```
## /api/entries/{tourn_id}/{event_id}
Takes a tournament id and event id as inputs and returns all entries.
### Example
```
http://127.0.0.1:8000/api/entries/26155/237918
```
```
{
  "entries": [
    {
      "school": "Arizona",
      "location": "AZ/US",
      "entry": "REDACTED",
      "code": "## REDACTED"
    },
    {
      "school": "Arizona",
      "location": "AZ/US",
      "entry": "REDACTED",
      "code": "## REDACTED"
    },
    ...
  ]
}
```

## /api/rounds/{tourn_id}/{event_id}
Takes a tournament id and event id as an inputs and returns all of the rounds and their respective IDs.
### Example
```
http://127.0.0.1:8000/api/rounds/26155/237918
```
```
{
  "rounds": [
    {
      "round_name": "OSWP Round 1",
      "round_id": "956623"
    },
    {
      "round_name": "OSWP Round 2",
      "round_id": "956624"
    },
    {
      "round_name": "OSWP Round 3",
      "round_id": "956625"
    },
    {
      "round_name": "OSWP Semi",
      "round_id": "956626"
    },
    {
      "round_name": "OSWP Final",
      "round_id": "956627"
    }
  ]
}
```


## /api/pairings/{tourn_id}/{round_id}
Takes a tournament id and round id as inputs and returns all pairings.
### Example
```
http://127.0.0.1:8000/api/pairings/26155/956626
```
```
{
  "entries": [
    {
      "": "1",
      "Room": "C203",
      "JudgesEntries": "REDACTED, REDACTED, REDACTED, REDACTED",
      "Entries": "1## REDACTED2## REDACTED3## REDACTED4## REDACTED5## REDACTED6## REDACTED"
    },
    {
     
      "": "2",
      "Room": "C203",
      "JudgesEntries": "REDACTED, REDACTED, REDACTED, REDACTED",
      "Entries": "1## REDACTED2## REDACTED3## REDACTED4## REDACTED5## REDACTED6## REDACTED"
    }
  ]
}
```





