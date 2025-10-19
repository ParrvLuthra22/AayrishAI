"""
JARVIS AI Assistant - AI API Manager
Handles communication with various AI services
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from config.settings import config_manager

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class AIResponse:
    """Standardized AI response format"""
    
    def __init__(self, text: str, model: str, tokens_used: int = 0, 
                 cost: float = 0.0, metadata: Dict[str, Any] = None):
        self.text = text
        self.model = model
        self.tokens_used = tokens_used
        self.cost = cost
        self.metadata = metadata or {}
        self.timestamp = datetime.now()

class AIAPIManager:
    """Manages communication with AI APIs"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.clients = {}
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize AI service clients"""
        
        if GROQ_AVAILABLE and config_manager.get_api_key("groq"):
            try:
                self.clients["groq"] = Groq(api_key=config_manager.get_api_key("groq"))
                self.logger.info("✅ Groq client initialized")
            except Exception as e:
                self.logger.error(f"❌ Groq initialization failed: {e}")
        
        if OPENAI_AVAILABLE and config_manager.get_api_key("openai"):
            try:
                openai.api_key = config_manager.get_api_key("openai")
                self.clients["openai"] = openai
                self.logger.info("✅ OpenAI client initialized")
            except Exception as e:
                self.logger.error(f"❌ OpenAI initialization failed: {e}")
        
        if ANTHROPIC_AVAILABLE and config_manager.get_api_key("anthropic"):
            try:
                self.clients["anthropic"] = Anthropic(api_key=config_manager.get_api_key("anthropic"))
                self.logger.info("✅ Anthropic client initialized")
            except Exception as e:
                self.logger.error(f"❌ Anthropic initialization failed: {e}")
        
        if GOOGLE_AVAILABLE and config_manager.get_api_key("google"):
            try:
                genai.configure(api_key=config_manager.get_api_key("google"))
                self.clients["google"] = genai
                self.logger.info("✅ Google Gemini client initialized")
            except Exception as e:
                self.logger.error(f"❌ Google Gemini initialization failed: {e}")
    
    async def query_ai(self, prompt: str, model: str = None, context: str = "", 
                      system_prompt: str = None) -> AIResponse:
        """Query an AI model"""
        
        if model is None:
            model = config_manager.ai.primary_model
        
        model = model.lower()
        
        try:
            if model == "groq" and "groq" in self.clients:
                return await self._query_groq(prompt, context, system_prompt)
            elif model == "openai" and "openai" in self.clients:
                return await self._query_openai(prompt, context, system_prompt)
            elif model == "claude" and "anthropic" in self.clients:
                return await self._query_claude(prompt, context, system_prompt)
            elif model == "gemini" and "google" in self.clients:
                return await self._query_gemini(prompt, context, system_prompt)
            else:
                for available_model in self.clients.keys():
                    self.logger.warning(f"Falling back to {available_model}")
                    return await self.query_ai(prompt, available_model, context, system_prompt)
                
                raise Exception("No AI models available")
                
        except Exception as e:
            self.logger.error(f"AI query failed: {e}")
            return AIResponse(
                text=f"I'm having trouble processing that request right now, {config_manager.get_user_name()}.",
                model=model,
                metadata={"error": str(e)}
            )
    
    async def _query_groq(self, prompt: str, context: str = "", system_prompt: str = None) -> AIResponse:
        """Query Groq AI"""
        client = self.clients["groq"]
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": f"""You are JARVIS, {config_manager.get_user_name()}'s advanced AI assistant. 
                Be helpful, intelligent, and concise. Always address the user as '{config_manager.get_user_name()}' or 'sir'.
                
                Context: {context}"""
            })
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = client.chat.completions.create(
                model=config_manager.ai.groq_model,
                messages=messages,
                temperature=config_manager.ai.temperature,
                max_tokens=config_manager.ai.max_tokens
            )
            
            response_text = completion.choices[0].message.content
            tokens_used = completion.usage.total_tokens if completion.usage else 0
            
            return AIResponse(
                text=response_text,
                model="groq",
                tokens_used=tokens_used
            )
            
        except Exception as e:
            raise Exception(f"Groq API error: {e}")
    
    async def _query_openai(self, prompt: str, context: str = "", system_prompt: str = None) -> AIResponse:
        """Query OpenAI GPT"""
        client = self.clients["openai"]
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system",
                "content": f"""You are JARVIS, {config_manager.get_user_name()}'s advanced AI assistant.
                Be helpful, intelligent, and concise. Always address the user as '{config_manager.get_user_name()}' or 'sir'.
                
                Context: {context}"""
            })
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await client.ChatCompletion.acreate(
                model=config_manager.ai.openai_model,
                messages=messages,
                temperature=config_manager.ai.temperature,
                max_tokens=config_manager.ai.max_tokens
            )
            
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            return AIResponse(
                text=response_text,
                model="openai",
                tokens_used=tokens_used
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    async def _query_claude(self, prompt: str, context: str = "", system_prompt: str = None) -> AIResponse:
        """Query Anthropic Claude"""
        client = self.clients["anthropic"]
        
        full_prompt = f"""
        {system_prompt if system_prompt else f"You are JARVIS, {config_manager.get_user_name()}'s advanced AI assistant. Be helpful, intelligent, and concise."}
        
        Context: {context}
        
        Human: {prompt}
        
        Assistant:"""
        
        try:
            response = client.completions.create(
                model=config_manager.ai.claude_model,
                prompt=full_prompt,
                max_tokens_to_sample=config_manager.ai.max_tokens,
                temperature=config_manager.ai.temperature
            )
            
            return AIResponse(
                text=response.completion,
                model="claude",
                tokens_used=0  
            )
            
        except Exception as e:
            raise Exception(f"Claude API error: {e}")
    
    async def _query_gemini(self, prompt: str, context: str = "", system_prompt: str = None) -> AIResponse:
        """Query Google Gemini"""
        genai = self.clients["google"]
        
        try:
            model = genai.GenerativeModel(config_manager.ai.gemini_model)
            
            full_prompt = f"""
            {system_prompt if system_prompt else f"You are JARVIS, {config_manager.get_user_name()}'s advanced AI assistant. Be helpful, intelligent, and concise."}
            
            Context: {context}
            
            User: {prompt}
            """
            
            response = model.generate_content(full_prompt)
            
            return AIResponse(
                text=response.text,
                model="gemini",
                tokens_used=0 
            )
            
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        return list(self.clients.keys())
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all AI services"""
        health_status = {}
        
        for model_name in self.clients.keys():
            try:
                response = await self.query_ai("Hello", model_name)
                health_status[model_name] = len(response.text) > 0
            except:
                health_status[model_name] = False
        
        return health_status

ai_manager = AIAPIManager()
