import requests

def get_weather(city='Kathmandu'):
    try:
        url= f"http://wttr.in/{city}?format=3"
        res = requests.get(url)
        if res.status_code==200:
            return res.text.strip()
        else:
            return f"Could not get weather for {city}."
    except Exception as e:
        return f"Weather tool error: {str(e)}"
    
    
def get_joke():
    try:
        url = "https://v2.jokeapi.dev/joke/Any"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if data["type"] == "single":
                return data["joke"]
            else:
                return f"{data['setup']} ... {data['delivery']}"
        else:
            return "Could not fetch a joke."
    except Exception as e:
        return f"Joke tool error: {str(e)}"
    
    
    
def get_quote():
    try:
        url = "https://api.quotable.io/random"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return f"\"{data['content']}\" – {data['author']}"
        else:
            return "Could not fetch a quote."
    except Exception as e:
        return f"Quote tool error: {str(e)}"
    
    
    
def search_wikipedia(query="Nepal"):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return f"{data['title']}: {data['extract']}"
        else:
            return f"No Wikipedia data found for {query}."
    except Exception as e:
        return f"Wikipedia tool error: {str(e)}"
    

    
def get_public_holidays(country="NP", year=2025):
    try:
        url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
        res = requests.get(url)
        if res.status_code == 200:
            holidays = res.json()[:5]
            return [f"{h['date']} – {h['localName']}" for h in holidays]
        else:
            return "Could not fetch holidays."
    except Exception as e:
        return f"Holiday tool error: {str(e)}"  
      