import re
import streamlit as st
import google.generativeai as genai
from src.tools import get_weather, get_joke, get_quote, search_wikipedia, get_public_holidays
from src.build_prompt import build_mcp_prompt

# ✅ Page Config
st.set_page_config(page_title="Sujan's MCP AI", page_icon="🤖", layout="centered")
st.title("🤖 Sujan's MCP AI Assistant")

# ✅ Session State Initialization
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "memory" not in st.session_state:
    st.session_state.memory = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Sidebar for Gemini API Key
st.sidebar.title("🔑 Gemini API Key")
if not st.session_state.api_key:
    api_key_input = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
    if st.sidebar.button("Save API Key") and api_key_input:
        try:
            genai.configure(api_key=api_key_input)
            test_model = genai.GenerativeModel("gemini-1.5-flash")
            test_model.generate_content("Hello")  # quick test
            st.session_state.api_key = api_key_input
            st.sidebar.success("✅ API Key saved successfully!")
        except Exception as e:
            st.sidebar.error(f"❌ Invalid API Key: {e}")
else:
    st.sidebar.success("✅ API Key already saved")
    if st.sidebar.button("Change API Key"):
        st.session_state.api_key = None
        st.session_state.chat_history = []
        st.session_state.memory = []
        st.rerun()

# ✅ Continue only if API Key is available
if st.session_state.api_key:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # ✅ MCP System Context
    system = "You are a helpful AI assistant made by Sujan Shrestha. Your task is to answer questions or call tools when needed."
    tools = """
    1. get_weather(city): Gets the weather using wttr.in. Example: get_weather(city="Kathmandu")
    2. get_joke(): Returns a random joke.
    3. get_quote(): Returns a random motivational quote.
    4. search_wikipedia(query): Returns a summary from Wikipedia. Example: search_wikipedia(query="Nepal")
    5. get_public_holidays(country, year): Returns public holidays for a given country and year. Example: get_public_holidays(country="NP", year=2025)
    """

    # ✅ Tool Handler
    def handle_tool_call(response):
        results, logs = [], []

        # Weather
        weather_match = re.search(r"get_weather\(city=['\"](.*?)['\"]\)", response)
        if weather_match:
            city = weather_match.group(1).strip()
            logs.append(f"🔧 Weather for {city}")
            results.append(f"Weather in {city}: {get_weather(city)}")

        # Joke
        if "get_joke()" in response:
            logs.append("🔧 Random Joke")
            results.append(f"Joke: {get_joke()}")

        # Quote
        if "get_quote()" in response:
            logs.append("🔧 Motivational Quote")
            results.append(f"Quote: {get_quote()}")

        # Wikipedia
        wiki_match = re.search(r"search_wikipedia\(query=['\"](.*?)['\"]\)", response)
        if wiki_match:
            query = wiki_match.group(1).strip()
            logs.append(f"🔧 Wikipedia search: {query}")
            results.append(f"Wikipedia Summary ({query}): {search_wikipedia(query)}")

        # Public Holidays
        holiday_match = re.search(r"get_public_holidays\(country=['\"](.*?)['\"],\s*year=(\d+)\)", response)
        if holiday_match:
            country = holiday_match.group(1).strip()
            year = int(holiday_match.group(2))
            logs.append(f"🔧 Public Holidays: {country} {year}")
            holidays = get_public_holidays(country, year)
            if isinstance(holidays, list):
                holidays = ", ".join(holidays)
            results.append(f"Holidays in {country} ({year}): {holidays}")
            
        
        # get_exchange_rate
        exchange_match = re.search(r"get_exchange_rate\(from_currency=['\"](.*?)['\"],\s*to_currency=['\"](.*?)['\"]\)", response)
        if exchange_match:
            from_currency = exchange_match.group(1).strip()
            to_currency = exchange_match.group(2).strip()
            print(f"[Tool] Getting exchange rate from {from_currency} to {to_currency}")
            results.append(f"Exchange rate from {from_currency} to {to_currency}: {get_exchange_rate(from_currency, to_currency)}")

        return "\n".join(results), "\n".join(logs) if results else (None, None)

    # ✅ Chat Interface
    st.markdown("---")
    user_input = st.text_input("💬 Ask me something:")

    if st.button("Ask") and user_input:
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
        for q, a in reversed(st.session_state.chat_history[-10:]):
            st.markdown(f"**You:** {q}")
            st.markdown(f"**AI:** {a}")
            st.markdown("---")
else:
    st.info("👈 Please enter your Gemini API key in the sidebar to start chatting.")
