"""
JARVIS AI Assistant - API Package
Handles external API integrations
"""

from .ai_manager import AIAPIManager, AIResponse, ai_manager
from .search_manager import WebSearchManager, SearchResult, search_manager

__all__ = ['AIAPIManager', 'AIResponse', 'ai_manager', 'WebSearchManager', 'SearchResult', 'search_manager']
