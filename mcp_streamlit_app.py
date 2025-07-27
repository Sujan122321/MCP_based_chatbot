import re
import streamlit as st
import google.generativeai as genai
from tools import *
from build_prompt import build_mcp_prompt

# ✅ Configure Gemini
genai.configure(api_key="AIzaSyCGv6JQnrQ8ORGnHNlDs6otwCq-Jv_vZb8")
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ MCP System Context
system = "You are a helpful AI assistant made by Sujan Shrestha. Your task is to answer questions or call tools when needed."
tools = """
1. get_weather(city): Gets the weather using wttr.in. Example: get_weather(city="Kathmandu")
2. get_joke(): Returns a random joke.
3. get_quote(): Returns a random motivational quote.
4. search_wikipedia(query): Returns a summary about the topic from Wikipedia. Example: search_wikipedia(query="Nepal")
5. get_public_holidays(country, year): Returns public holidays for a given country and year. Example: get_public_holidays(country="NP", year=2025)
6. get_exchange_rate(from_currency, to_currency): Returns the exchange rate between two currencies. Example: get_exchange_rate(from_currency="USD", to_currency="EUR")

"""

# ✅ Session State for Memory
if "memory" not in st.session_state:
    st.session_state.memory = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Tool Handler
def handle_tool_call(response):
    results = []
    logs = []

    # Weather
    weather_match = re.search(r"get_weather\(city=['\"](.*?)['\"]\)", response)
    if weather_match:
        city = weather_match.group(1).strip()
        logs.append(f"🔧 Tool: Weather for {city}")
        results.append(f"Weather in {city}: {get_weather(city)}")

    # Joke
    if "get_joke()" in response:
        logs.append("🔧 Tool: Random Joke")
        results.append(f"Joke: {get_joke()}")

    # Quote
    if "get_quote()" in response:
        logs.append("🔧 Tool: Motivational Quote")
        results.append(f"Quote: {get_quote()}")

    # Wikipedia
    wiki_match = re.search(r"search_wikipedia\(query=['\"](.*?)['\"]\)", response)
    if wiki_match:
        query = wiki_match.group(1).strip()
        logs.append(f"🔧 Tool: Wikipedia search for {query}")
        results.append(f"Wikipedia Summary ({query}): {search_wikipedia(query)}")

    # Public Holidays
    holiday_match = re.search(r"get_public_holidays\(country=['\"](.*?)['\"],\s*year=(\d+)\)", response)
    if holiday_match:
        country = holiday_match.group(1).strip()
        year = int(holiday_match.group(2))
        logs.append(f"🔧 Tool: Public Holidays for {country} in {year}")
        holidays = get_public_holidays(country, year)
        if isinstance(holidays, list):
            holidays = ", ".join(holidays)
        results.append(f"Holidays in {country} ({year}): {holidays}")
        
    # Exchange Rate# get_exchange_rate
    exchange_match = re.search(r"get_exchange_rate\(from_currency=['\"](.*?)['\"],\s*to_currency=['\"](.*?)['\"]\)", response)
    if exchange_match:
        from_currency = exchange_match.group(1).strip()
        to_currency = exchange_match.group(2).strip()
        print(f"[Tool] Getting exchange rate from {from_currency} to {to_currency}")
        results.append(f"Exchange rate from {from_currency} to {to_currency}: {get_exchange_rate(from_currency, to_currency)}")

    return "\n".join(results), "\n".join(logs) if results else (None, None)

# ✅ Streamlit UI
st.set_page_config(page_title="Sujan's MCP AI", page_icon="🤖", layout="centered")
st.title("🤖 Sujan's MCP AI Assistant")
st.markdown("Ask me anything! I can tell jokes, weather, Wikipedia info, quotes, or public holidays.")

user_input = st.text_input("Type your question here:")

if st.button("Ask") and user_input:
    # Build MCP Prompt
    prompt = build_mcp_prompt(system, tools, user_input, st.session_state.memory)
    response = model.generate_content(prompt).text

    tool_output, logs = handle_tool_call(response)

    if tool_output:
        followup_prompt = (
            f"The user asked: {user_input}\n"
            f"The tool returned:\n{tool_output}\n\n"
            f"Respond naturally to the user using these results."
        )
        final_response = model.generate_content(followup_prompt).text
    else:
        final_response = response

    # Save chat history
    st.session_state.chat_history.append((user_input, final_response))
    st.session_state.memory.append(f"User: {user_input}")
    st.session_state.memory.append(f"AI: {final_response}")

    # Display logs (optional)
    if logs:
        with st.expander("🔧 Tool Logs"):
            st.text(logs)

# ✅ Display Chat History
if st.session_state.chat_history:
    st.subheader("💬 Chat History")
    for q, a in reversed(st.session_state.chat_history[-10:]):  # show last 10 exchanges
        st.markdown(f"**You:** {q}")
        st.markdown(f"**AI:** {a}")
        st.markdown("---")
