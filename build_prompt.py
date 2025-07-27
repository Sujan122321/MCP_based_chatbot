def build_mcp_prompt(system, tools, query, memory=[]):
    prompt =""
    
    prompt += f"System: {system}\n"
    prompt += f"Available tools: \n{tools}\n\n"
    if memory:
        prompt +="Memory:\n" + "\n".join(memory) + "\n\n"
    prompt += f"User Query: \n{query}\n\n"
    
    prompt += (
        "Instructions: \n"
        "1. If the query is about weather, respond ONLY with a code block like this:\n"
        "```tool_code\nget_weather(city='CityName')\n```\n"""
        "2. If multiple tools are needed, put each call on a new line inside the same code block.\n"
        "3. If the query is about currency exchange rate, respond ONLY with a code block like this:\n"
        "```tool_code\nget_exchange_rate(from_currency='FromCurrency', to_currency='ToCurrency')\n```\n"
        "4. If no tool is relevant, reply in natural language.\n"
        "Otherwise, reply normally.\n"
    )
    
    return prompt
    