# Standard Library Imports
from datetime import datetime

# Third-Party Library Imports
from langchain.tools import tool

# Local Application Imports

@tool
def save_text_to_file_tool(data: str, filename: str = "research_output.txt"):
    "Save structured research data to a text file"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"