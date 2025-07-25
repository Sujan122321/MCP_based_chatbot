import re
import google.generativeai as genai
from tools import get_weather
from build_prompt import build_mcp_prompt

genai.configure(api_key="AIzaSyCGv6JQnrQ8ORGnHNlDs6otwCq-Jv_vZb8")
model = genai.GenerativeModel("gemini-1.5-flash")

# MCP Context
system = "You are a helpful ai assistant made by sujan shrestha. Your task is to answer question."
tools = "get_weather(city) : Gets the weather using wttr. in.  Call only when asked about weather."
memory =[]
 
def handle_tool_call(response):
    pattern = r"```tool_code\s*\nget_weather\(city=['\"](.*?)['\"]\)\s*```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        city = match.group(1).strip()
        print(f"[Tool] Getting weather for: {city}")
        return get_weather(city)
    return None

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