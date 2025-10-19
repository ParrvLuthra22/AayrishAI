"""
JARVIS AI Assistant - Core Brain
The central intelligence that processes commands and coordinates responses
"""

import asyncio
import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass

from config.settings import config_manager

@dataclass
class Intent:
    """Represents a recognized intent"""
    name: str
    confidence: float
    entities: Dict[str, Any]
    raw_text: str

@dataclass
class Context:
    """Conversation context"""
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, str]]
    user_preferences: Dict[str, Any]
    active_tasks: List[str]

class IntentRecognizer:
    """Recognizes user intents from natural language"""
    
    def __init__(self):
        self.intent_patterns = {
            "system_control": [
                r"(open|launch|start)\s+(.+)",
                r"(close|quit|exit)\s+(.+)",
                r"(shutdown|restart|sleep)\s*(computer|system|mac)?",
                r"(increase|decrease|set)\s+(volume|brightness)",
                r"show\s+(notifications|calendar|weather)"
            ],
            "web_search": [
                r"(search|look up|find|google)\s+(.+)",
                r"what is\s+(.+)",
                r"who is\s+(.+)",
                r"tell me about\s+(.+)",
                r"(news|weather|stock)\s*(for|about)?\s*(.+)?"
            ],
            "ai_query": [
                r"(ask|query)\s+(chatgpt|claude|gemini|gpt)\s+(.+)",
                r"(chatgpt|claude|gemini|gpt),?\s+(.+)",
                r"generate\s+(.+)",
                r"explain\s+(.+)",
                r"summarize\s+(.+)"
            ],
            "communication": [
                r"(send|text|message)\s+(.+)\s+(to|that)\s+(.+)",
                r"(email|mail)\s+(.+)\s+(to|that)\s+(.+)",
                r"call\s+(.+)",
                r"remind me\s+(to\s+)?(.+)"
            ],
            "file_operations": [
                r"(create|make|new)\s+(file|folder|document)\s+(.+)",
                r"(delete|remove)\s+(.+)",
                r"(copy|move)\s+(.+)\s+(to|into)\s+(.+)",
                r"(read|open|show)\s+(file|document)\s+(.+)"
            ],
            "conversation": [
                r"(hello|hi|hey|good morning|good evening)",
                r"how are you",
                r"what can you do",
                r"help",
                r"thank you|thanks"
            ]
        }
    
    async def recognize_intent(self, text: str) -> Intent:
        """Recognize intent from user input"""
        text = text.lower().strip()
        
        wake_word = config_manager.voice.wake_word.lower()
        if text.startswith(wake_word):
            text = text[len(wake_word):].strip()
        
        best_intent = None
        best_confidence = 0.0
        best_entities = {}
        
        for intent_name, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    confidence = self._calculate_confidence(text, pattern)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent_name
                        best_entities = self._extract_entities(match, intent_name)
        
        if best_intent is None:
            best_intent = "conversation"
            best_confidence = 0.5
        
        return Intent(
            name=best_intent,
            confidence=best_confidence,
            entities=best_entities,
            raw_text=text
        )
    
    def _calculate_confidence(self, text: str, pattern: str) -> float:
        """Calculate confidence score for pattern match"""
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return 0.0
        
        match_length = len(match.group(0))
        text_length = len(text)
        base_confidence = match_length / text_length
        
        if match.start() == 0:
            base_confidence += 0.2
        
        return min(base_confidence, 1.0)
    
    def _extract_entities(self, match: re.Match, intent_name: str) -> Dict[str, Any]:
        """Extract entities from regex match"""
        entities = {}
        groups = match.groups()
        
        if intent_name == "system_control":
            if len(groups) >= 2:
                entities["action"] = groups[0]
                entities["target"] = groups[1]
        
        elif intent_name == "web_search":
            if len(groups) >= 1:
                entities["query"] = groups[-1] if groups[-1] else groups[0]
        
        elif intent_name == "ai_query":
            if len(groups) >= 2:
                entities["model"] = groups[0]
                entities["query"] = groups[1]
            elif len(groups) >= 1:
                entities["query"] = groups[0]
        
        elif intent_name == "communication":
            if len(groups) >= 3:
                entities["action"] = groups[0]
                entities["message"] = groups[1]
                entities["recipient"] = groups[2]
        
        elif intent_name == "file_operations":
            if len(groups) >= 2:
                entities["action"] = groups[0]
                entities["target"] = groups[1]
                if len(groups) >= 4:
                    entities["destination"] = groups[3]
        
        return entities

class ConversationMemory:
    """Manages conversation context and memory"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversations: Dict[str, Context] = {}
    
    def get_context(self, user_id: str, session_id: str) -> Context:
        """Get or create conversation context"""
        key = f"{user_id}_{session_id}"
        
        if key not in self.conversations:
            self.conversations[key] = Context(
                user_id=user_id,
                session_id=session_id,
                conversation_history=[],
                user_preferences=config_manager.user_preferences.copy(),
                active_tasks=[]
            )
        
        return self.conversations[key]
    
    def add_exchange(self, user_id: str, session_id: str, user_input: str, assistant_response: str):
        """Add conversation exchange to memory"""
        context = self.get_context(user_id, session_id)
        
        context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        })
        
        # Keep only recent history
        if len(context.conversation_history) > self.max_history:
            context.conversation_history = context.conversation_history[-self.max_history:]
    
    def get_conversation_summary(self, user_id: str, session_id: str) -> str:
        """Get conversation summary for context"""
        context = self.get_context(user_id, session_id)
        
        if not context.conversation_history:
            return "This is the start of our conversation."
        
        recent_exchanges = context.conversation_history[-3:]
        summary = "Recent conversation:\n"
        
        for exchange in recent_exchanges:
            summary += f"User: {exchange['user']}\n"
            summary += f"Assistant: {exchange['assistant']}\n"
        
        return summary

class JarvisBrain:
    """The central intelligence of JARVIS"""
    
    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.memory = ConversationMemory()
        self.skill_handlers = {}
        self.logger = logging.getLogger(__name__)
        self._initialize_skills()
        
        self._initialize_skills()
    
    def register_skill(self, intent_name: str, handler):
        """Register a skill handler for an intent"""
        self.skill_handlers[intent_name] = handler
        self.logger.info(f"Registered skill handler for intent: {intent_name}")
    
    def _initialize_skills(self):
        """Initialize and register all available skills"""
        try:
            from skills.skill_manager import (
                SystemControlSkill, WebSearchSkill, AIQuerySkill, 
                FileOperationsSkill, SkillManager
            )
            
            skills = [
                SystemControlSkill(),
                WebSearchSkill(),
                AIQuerySkill(),
                FileOperationsSkill()
            ]
            
            intent_skill_map = {
                "system_control": skills[0],
                "web_search": skills[1], 
                "ai_query": skills[2],
                "conversation": skills[2],
                "file_operations": skills[3]
            }
            
            for intent_name, skill in intent_skill_map.items():
                self.register_skill(intent_name, skill)
                
            self.logger.info(f"✅ Initialized {len(skills)} skills with {len(intent_skill_map)} intent mappings")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing skills: {e}")
    
    async def process_input(self, user_input: str, user_id: str = "default", session_id: str = "main") -> Dict[str, Any]:
        """Process user input and generate response"""
        try:
            intent = await self.intent_recognizer.recognize_intent(user_input)
            self.logger.info(f"Recognized intent: {intent.name} (confidence: {intent.confidence:.2f})")
            context = self.memory.get_context(user_id, session_id)
            if intent.name in self.skill_handlers:
                handler = self.skill_handlers[intent.name]
                response = await handler.handle(intent, context)
            else:
                response = {
                    "text": f"I understand you want me to handle '{intent.name}', but I don't have that capability yet, {config_manager.get_user_name()}.",
                    "actions": [],
                    "data": {}
                }
            
            self.memory.add_exchange(user_id, session_id, user_input, response.get("text", ""))
            
            return {
                "intent": intent,
                "response": response,
                "context": context
            }
            
        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return {
                "intent": Intent("error", 0.0, {}, user_input),
                "response": {
                    "text": f"I encountered an error processing your request, {config_manager.get_user_name()}. Please try again.",
                    "actions": [],
                    "data": {"error": str(e)}
                },
                "context": self.memory.get_context(user_id, session_id)
            }

jarvis_brain = JarvisBrain()
