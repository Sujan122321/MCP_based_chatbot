# MCP_based_chatbot

## Overview
**MCP_based_chatbot** is a modular chatbot application built with Python. It is designed to be easy to extend and customize, making it suitable for learning, prototyping, or integrating into larger systems.

## Features
- Modular structure for adding or updating chatbot modules
- Uses modern NLP tools to understand user input
- Customizable responses for different domains
- Ready for integration with external APIs or data sources

## Technologies Used
- Python 3.12
- Gemini flash-2.0 lite
- Visual Studio Code (code edior)
- Other dependencies listed in `requirements.txt`
- Weather, currency translation and other tools are used 

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/MCP_based_chatbot.git
   ```
2. Go to the project folder:
   ```sh
   cd MCP_based_chatbot
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Start the chatbot:
   ```sh
   streamlit run mcp_app.py
   ```
2. Enter your Gemini api key 
3. Type your questions in the terminal and get responses.


## Project Structure

```
MCP_based_chatbot/
├── mcp_app.py            # Main chatbot script
├── simple_test_app.py    # Test app without streamlit
├── src/                  # Chatbot modules
│   └── __init__.py       # Module initializer
│   └── tools.py          # Utility functions
│   └── build_prompt.py   # Prompt builder
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Contributing

Feel free to open issues or submit pull requests for improvements. Please follow the project style and add documentation where needed.

## License

MIT License

## Contact

For questions or support, please contact