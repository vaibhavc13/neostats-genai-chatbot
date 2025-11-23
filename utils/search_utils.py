from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def perform_web_search(query: str) -> str:
    """
    Perform a web search using DuckDuckGo.
    """
    try:
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
        search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        results = search.invoke(query)
        return results
    except Exception as e:
        return f"Error performing web search: {str(e)}"
