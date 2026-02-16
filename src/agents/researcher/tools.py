from typing import List, Dict, Any

class MockSearchTool:
    """
    A tool that mocks Google Search results.
    Follows a simple callable interface that can be wrapped as an MCP tool later.
    """

    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Performs a mock search for the given query.

        Args:
            query: The search query string.

        Returns:
            A list of search results with title, snippet, and url.
        """
        print(f"[MockSearchTool] Searching for: {query}")

        # Simple keyword-based mock responses to simulate diverse viewpoints
        results = []

        q = query.lower()
        if "webrtc" in q:
            results.append({
                "title": "The Future of WebRTC: AI Codecs",
                "snippet": "New AI-driven codecs are set to revolutionize real-time communication latency and quality.",
                "url": "https://webrtc.org/ai-codecs"
            })
            results.append({
                "title": "Is WebTransport the End of WebRTC?",
                "snippet": "Developers are shifting to WebTransport for more flexibility, arguing WebRTC is becoming obsolete.",
                "url": "https://techcrunch.com/webtransport-vs-webrtc"
            })
            results.append({
                "title": "WebRTC 2.0 Specifications Released",
                "snippet": "W3C announces new standards for end-to-end encryption and peer-to-peer data channels.",
                "url": "https://w3c.org/webrtc-2.0"
            })
        elif "podcast" in q:
             results.append({
                "title": "Podcasting Trends 2025",
                "snippet": "AI-generated hosts are gaining popularity, but human connection remains key.",
                "url": "https://podcast-insider.com/trends"
            })
        else:
            results.append({
                "title": f"General Information about {query}",
                "snippet": f"This is a placeholder result for the topic {query}. It contains general facts.",
                "url": f"https://encyclopedia.com/{query.replace(' ', '_')}"
            })

        return results

# Function wrapper for ADK
def google_search(query: str) -> List[Dict[str, Any]]:
    """
    Searches the web for the given query.
    """
    tool = MockSearchTool()
    return tool.search(query)
