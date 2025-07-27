import re
import google.generativeai as genai
from tools import *
from build_prompt import build_mcp_prompt

genai.configure(api_key="AIzaSyCGv6JQnrQ8ORGnHNlDs6otwCq-Jv_vZb8")
model = genai.GenerativeModel("gemini-1.5-flash")

# MCP Context
system = "You are a helpful ai assistant made by sujan shrestha. Your task is to answer question."
tools= """
    1. get_weather(city) : Gets the weather using wttr. in.  Call only when asked about weather."
    2. get_joke(): Returns a random joke.
    3. get_quote(): Returns a random motivational quote.
    4. search_wikipedia(query): Returns a summary about the topic from Wikipedia. Example: search_wikipedia(query="Nepal")
    5. get_public_holidays(country, year): Returns public holidays for a given country and year. Example: get_public_holidays(country="NP", year=2025)
    6. get_exchange_rate(from_currency, to_currency): Returns the exchange rate between two currencies. Example: get_exchange_rate(from_currency="USD", to_currency="EUR")
"""
memory =[]
 
# ✅ Handle multiple tool calls
def handle_tool_call(response):
    results = []
    
    # get_weather
    weather_match = re.search(r"get_weather\(city=['\"](.*?)['\"]\)", response)
    if weather_match:
        city = weather_match.group(1).strip()
        print(f"[Tool] Getting weather for: {city}")
        results.append(f"Weather in {city}: {get_weather(city)}")

    # get_joke
    if "get_joke()" in response:
        print("[Tool] Getting a random joke")
        results.append(f"Joke: {get_joke()}")

    # get_quote
    if "get_quote()" in response:
        print("[Tool] Getting a motivational quote")
        results.append(f"Quote: {get_quote()}")

    # search_wikipedia
    wiki_match = re.search(r"search_wikipedia\(query=['\"](.*?)['\"]\)", response)
    if wiki_match:
        query = wiki_match.group(1).strip()
        print(f"[Tool] Searching Wikipedia for: {query}")
        results.append(f"Wikipedia Summary ({query}): {search_wikipedia(query)}")

    # get_public_holidays
    holiday_match = re.search(r"get_public_holidays\(country=['\"](.*?)['\"],\s*year=(\d+)\)", response)
    if holiday_match:
        country = holiday_match.group(1).strip()
        year = int(holiday_match.group(2))
        print(f"[Tool] Getting public holidays for {country} in {year}")
        results.append(f"Holidays in {country} ({year}): {get_public_holidays(country, year)}")
    
    # get_exchange_rate
    exchange_match = re.search(r"get_exchange_rate\(from_currency=['\"](.*?)['\"],\s*to_currency=['\"](.*?)['\"]\)", response)
    if exchange_match:
        from_currency = exchange_match.group(1).strip()
        to_currency = exchange_match.group(2).strip()
        print(f"[Tool] Getting exchange rate from {from_currency} to {to_currency}")
        results.append(f"Exchange rate from {from_currency} to {to_currency}: {get_exchange_rate(from_currency, to_currency)}")

    return "\n".join(results) if results else None

# Main Loop
if __name__ == "__main__":
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        
        prompt = build_mcp_prompt(system, tools, user_input, memory)
        response = model.generate_content(prompt).text
        
        tool_output = handle_tool_call(response)
        
        if tool_output:
            followup_prompt = (
                f"The user asked: {user_input}\n"
                f"The tool returned: {tool_output}\n"
                f"Respond to the user naturally using this result:"
            )
            final_response = model.generate_content(followup_prompt).text
        
            print("\nGemini:", final_response)
            memory.append(f"User:{user_input}\n")
            memory.append(f"AI: {final_response}\n")
        else:
            print("\nGemini:", response)
            memory.append(f"User:{user_input}\n")
            memory.append(f"AI: {response}\n")