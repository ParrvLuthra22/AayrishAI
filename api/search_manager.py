"""
JARVIS AI Assistant - Web Search Manager
Handles web searches and information retrieval
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from config.settings import config_manager

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

class SearchResult:
    """Standardized search result format"""
    
    def __init__(self, title: str, url: str, snippet: str, source: str = "", 
                 confidence: float = 1.0, metadata: Dict[str, Any] = None):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source
        self.confidence = confidence
        self.metadata = metadata or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }

class WebSearchManager:
    """Manages web searches across multiple providers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.search_engines = {}
        self.initialize_engines()
    
    def initialize_engines(self):
        """Initialize search engine clients"""
        
        # DuckDuckGo Search
        if DDGS_AVAILABLE:
            try:
                self.search_engines["duckduckgo"] = DDGS()
                self.logger.info("✅ DuckDuckGo search initialized")
            except Exception as e:
                self.logger.error(f"❌ DuckDuckGo initialization failed: {e}")
        
        # Tavily Search
        if TAVILY_AVAILABLE and config_manager.get_api_key("tavily"):
            try:
                self.search_engines["tavily"] = TavilyClient(api_key=config_manager.get_api_key("tavily"))
                self.logger.info("✅ Tavily search initialized")
            except Exception as e:
                self.logger.error(f"❌ Tavily initialization failed: {e}")
        
        # Wikipedia is always available as fallback
        if WIKIPEDIA_AVAILABLE:
            self.search_engines["wikipedia"] = True
            self.logger.info("✅ Wikipedia search available")
    
    async def search(self, query: str, max_results: int = 5, 
                    search_type: str = "general") -> List[SearchResult]:
        """Perform web search"""
        
        results = []
        
        try:
            # Try Tavily first for comprehensive results
            if "tavily" in self.search_engines and search_type == "general":
                tavily_results = await self._search_tavily(query, max_results)
                results.extend(tavily_results)
            
            # Use DuckDuckGo for broader search
            if "duckduckgo" in self.search_engines and len(results) < max_results:
                ddg_results = await self._search_duckduckgo(query, max_results - len(results))
                results.extend(ddg_results)
            
            # Wikipedia for factual information
            if "wikipedia" in self.search_engines and search_type in ["factual", "general"]:
                wiki_results = await self._search_wikipedia(query, 2)
                results.extend(wiki_results)
            
            # Remove duplicates and sort by confidence
            results = self._deduplicate_results(results)
            results.sort(key=lambda x: x.confidence, reverse=True)
            
            return results[:max_results]
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    async def _search_tavily(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Tavily API"""
        try:
            client = self.search_engines["tavily"]
            response = client.search(query, search_depth="basic", max_results=max_results)
            
            results = []
            for item in response.get("results", []):
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("content", ""),
                    source="tavily",
                    confidence=item.get("score", 0.8),
                    metadata={"published_date": item.get("published_date")}
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.warning(f"Tavily search failed: {e}")
            return []
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo"""
        try:
            ddgs = self.search_engines["duckduckgo"]
            search_results = ddgs.text(query, max_results=max_results)
            
            results = []
            for item in search_results:
                result = SearchResult(
                    title=item.get("title", ""),
                    url=item.get("href", ""),
                    snippet=item.get("body", ""),
                    source="duckduckgo",
                    confidence=0.7
                )
                results.append(result)
            
            return results
            
        except Exception as e:
            self.logger.warning(f"DuckDuckGo search failed: {e}")
            return []
    
    async def _search_wikipedia(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Wikipedia"""
        try:
            # Search for pages
            search_results = wikipedia.search(query, results=max_results)
            
            results = []
            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title)
                    summary = wikipedia.summary(title, sentences=2)
                    
                    result = SearchResult(
                        title=page.title,
                        url=page.url,
                        snippet=summary,
                        source="wikipedia",
                        confidence=0.9,
                        metadata={"page_id": page.pageid}
                    )
                    results.append(result)
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Try the first option
                    if e.options:
                        try:
                            page = wikipedia.page(e.options[0])
                            summary = wikipedia.summary(e.options[0], sentences=2)
                            
                            result = SearchResult(
                                title=page.title,
                                url=page.url,
                                snippet=summary,
                                source="wikipedia",
                                confidence=0.8
                            )
                            results.append(result)
                        except:
                            continue
                except:
                    continue
            
            return results
            
        except Exception as e:
            self.logger.warning(f"Wikipedia search failed: {e}")
            return []
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate search results"""
        seen_urls = set()
        seen_titles = set()
        unique_results = []
        
        for result in results:
            # Check for duplicate URLs or very similar titles
            if result.url not in seen_urls and result.title.lower() not in seen_titles:
                seen_urls.add(result.url)
                seen_titles.add(result.title.lower())
                unique_results.append(result)
        
        return unique_results
    
    async def get_news(self, topic: str = "", max_results: int = 5) -> List[SearchResult]:
        """Get latest news"""
        query = f"latest news {topic}".strip()
        return await self.search(query, max_results, "news")
    
    async def get_weather(self, location: str = "") -> Dict[str, Any]:
        """Get weather information"""
        query = f"weather {location}".strip()
        results = await self.search(query, 3, "weather")
        
        weather_info = {
            "location": location,
            "summary": "",
            "source": "",
            "details": []
        }
        
        if results:
            weather_info["summary"] = results[0].snippet
            weather_info["source"] = results[0].source
            weather_info["details"] = [r.to_dict() for r in results]
        
        return weather_info
    
    async def fact_check(self, claim: str) -> List[SearchResult]:
        """Fact-check a claim"""
        query = f"fact check {claim}"
        return await self.search(query, 5, "factual")
    
    def get_available_engines(self) -> List[str]:
        """Get list of available search engines"""
        return list(self.search_engines.keys())

# Global search manager instance
search_manager = WebSearchManager()
