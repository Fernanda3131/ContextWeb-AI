from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from datetime import datetime

search_Duck = DuckDuckGoSearchRun()

search_wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=2), doc_content_chars_max=500) 

@tool
def save_to_txt(data: str, filename: str = "research_output.txt"):
    """Saves structure research data to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
        
    return f"Data successfully saved to {filename}"
