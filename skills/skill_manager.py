"""
JARVIS AI Assistant - Skill Manager
Manages and coordinates all JARVIS skills and capabilities
"""

import logging
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

from core.brain import Intent, Context

class BaseSkill(ABC):
    """Base class for all JARVIS skills"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"SKILL_{name.upper()}")
    
    @abstractmethod
    async def handle(self, intent: Intent, context: Context) -> Dict[str, Any]:
        """Handle the intent and return response"""
        pass
    
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """Check if this skill can handle the intent"""
        pass
    
    def get_help(self) -> str:
        """Get help text for this skill"""
        return f"{self.name}: {self.description}"

class SystemControlSkill(BaseSkill):
    """System control and automation skill"""
    
    def __init__(self):
        super().__init__(
            name="SystemControl",
            description="Control macOS system functions like opening apps, shutdown, volume control"
        )
    
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "system_control"
    
    async def handle(self, intent: Intent, context: Context) -> Dict[str, Any]:
        """Handle system control commands"""
        action = intent.entities.get("action", "").lower()
        target = intent.entities.get("target", "").lower()
        
        self.logger.info(f"System control: {action} {target}")
        
        try:
            import subprocess
            
            if action in ["open", "launch", "start"]:
                return await self._open_application(target)
            elif action in ["close", "quit", "exit"]:
                return await self._close_application(target)
            elif action in ["shutdown", "shut down"]:
                return await self._shutdown_system()
            elif action == "restart":
                return await self._restart_system()
            elif action == "sleep":
                return await self._sleep_system()
            elif "volume" in intent.raw_text.lower():
                return await self._control_volume(intent.raw_text)
            else:
                return {
                    "text": f"I'm not sure how to {action} {target}, {context.user_preferences.get('name', 'User')}.",
                    "actions": [],
                    "data": {}
                }
                
        except Exception as e:
            self.logger.error(f"System control error: {e}")
            return {
                "text": f"I encountered an error with that system command, {context.user_preferences.get('name', 'User')}.",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _open_application(self, app_name: str) -> Dict[str, Any]:
        """Open an application"""
        app_mapping = {
            "safari": "Safari",
            "chrome": "Google Chrome",
            "firefox": "Firefox",
            "finder": "Finder",
            "mail": "Mail",
            "music": "Music",
            "spotify": "Spotify",
            "terminal": "Terminal",
            "calculator": "Calculator",
            "notes": "Notes",
            "calendar": "Calendar",
            "photos": "Photos",
            "messages": "Messages",
            "facetime": "FaceTime",
            "zoom": "zoom.us",
            "slack": "Slack",
            "discord": "Discord",
            "vscode": "Visual Studio Code",
            "code": "Visual Studio Code",
            "xcode": "Xcode"
        }
        
        actual_app = app_mapping.get(app_name, app_name.title())
        
        try:
            import subprocess
            result = subprocess.run(
                ['osascript', '-e', f'tell application "{actual_app}" to activate'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "text": f"Opening {actual_app} for you, sir.",
                    "actions": ["app_opened"],
                    "data": {"app": actual_app}
                }
            else:
                return {
                    "text": f"I couldn't find or open {actual_app}. Please check if it's installed.",
                    "actions": [],
                    "data": {"error": result.stderr}
                }
                
        except Exception as e:
            return {
                "text": f"Error opening {actual_app}: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _close_application(self, app_name: str) -> Dict[str, Any]:
        """Close an application"""
        try:
            import subprocess
            result = subprocess.run(
                ['osascript', '-e', f'tell application "{app_name.title()}" to quit'],
                capture_output=True, text=True, timeout=10
            )
            
            return {
                "text": f"Closing {app_name.title()} for you, sir.",
                "actions": ["app_closed"],
                "data": {"app": app_name.title()}
            }
            
        except Exception as e:
            return {
                "text": f"Error closing {app_name}: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _shutdown_system(self) -> Dict[str, Any]:
        """Shutdown the system"""
        try:
            import subprocess
            subprocess.run(['osascript', '-e', 'tell application "System Events" to shut down'])
            return {
                "text": "Shutting down the system, sir. Goodbye.",
                "actions": ["system_shutdown"],
                "data": {}
            }
        except Exception as e:
            return {
                "text": f"Error shutting down: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _restart_system(self) -> Dict[str, Any]:
        """Restart the system"""
        try:
            import subprocess
            subprocess.run(['osascript', '-e', 'tell application "System Events" to restart'])
            return {
                "text": "Restarting the system, sir.",
                "actions": ["system_restart"],
                "data": {}
            }
        except Exception as e:
            return {
                "text": f"Error restarting: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _sleep_system(self) -> Dict[str, Any]:
        """Put system to sleep"""
        try:
            import subprocess
            subprocess.run(['osascript', '-e', 'tell application "System Events" to sleep'])
            return {
                "text": "Putting the system to sleep, sir.",
                "actions": ["system_sleep"],
                "data": {}
            }
        except Exception as e:
            return {
                "text": f"Error putting system to sleep: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _control_volume(self, command: str) -> Dict[str, Any]:
        """Control system volume"""
        try:
            import subprocess
            
            if "increase" in command or "up" in command:
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
                return {
                    "text": "Volume increased, sir.",
                    "actions": ["volume_changed"],
                    "data": {"direction": "up"}
                }
            elif "decrease" in command or "down" in command:
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
                return {
                    "text": "Volume decreased, sir.",
                    "actions": ["volume_changed"],
                    "data": {"direction": "down"}
                }
            elif "mute" in command:
                subprocess.run(['osascript', '-e', 'set volume with output muted'])
                return {
                    "text": "Volume muted, sir.",
                    "actions": ["volume_muted"],
                    "data": {}
                }
            else:
                return {
                    "text": "I'm not sure how to adjust the volume that way, sir.",
                    "actions": [],
                    "data": {}
                }
                
        except Exception as e:
            return {
                "text": f"Error controlling volume: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }

class WebSearchSkill(BaseSkill):
    """Web search and information retrieval skill"""
    
    def __init__(self):
        super().__init__(
            name="WebSearch",
            description="Search the web for information, news, weather, and facts"
        )
    
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "web_search"
    
    async def handle(self, intent: Intent, context: Context) -> Dict[str, Any]:
        """Handle web search requests"""
        query = intent.entities.get("query", intent.raw_text)
        
        self.logger.info(f"Web search: {query}")
        
        try:
            from api import search_manager
            
            # Perform search
            results = await search_manager.search(query, max_results=3)
            
            if results:
                # Format response
                response_text = f"Here's what I found about {query}:\n\n"
                
                for i, result in enumerate(results[:2], 1):
                    response_text += f"{i}. {result.title}\n{result.snippet[:150]}...\n\n"
                
                return {
                    "text": response_text.strip(),
                    "actions": ["web_search_completed"],
                    "data": {
                        "query": query,
                        "results": [r.to_dict() for r in results],
                        "source": "web_search"
                    }
                }
            else:
                return {
                    "text": f"I couldn't find any information about {query} right now, sir. Please try rephrasing your search.",
                    "actions": [],
                    "data": {"query": query, "results": []}
                }
                
        except Exception as e:
            self.logger.error(f"Web search error: {e}")
            return {
                "text": f"I encountered an error while searching the web, sir: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }

class AIQuerySkill(BaseSkill):
    """AI model query and conversation skill"""
    
    def __init__(self):
        super().__init__(
            name="AIQuery",
            description="Query specific AI models and handle general conversation"
        )
    
    def can_handle(self, intent: Intent) -> bool:
        return intent.name in ["ai_query", "conversation"]
    
    async def handle(self, intent: Intent, context: Context) -> Dict[str, Any]:
        """Handle AI queries and conversation"""
        query = intent.entities.get("query", intent.raw_text)
        model = intent.entities.get("model", "auto").lower()
        
        self.logger.info(f"AI query: {query} (model: {model})")
        
        # Simple conversation responses for common queries
        query_lower = query.lower()
        if any(greeting in query_lower for greeting in ["hello", "hi", "hey"]):
            return {
                "text": "Hello Mr. Luthra! I'm JARVIS, your AI assistant. How may I help you today?",
                "actions": ["greeting_response"],
                "data": {"query": query}
            }
        elif any(phrase in query_lower for phrase in ["how are you", "how's it going"]):
            return {
                "text": "I'm functioning optimally, sir. All systems are running smoothly. How can I assist you?",
                "actions": ["status_response"],
                "data": {"query": query}
            }
        elif "what can you do" in query_lower or "help" in query_lower:
            return {
                "text": "I can help you with system control, web searches, file operations, and general conversation. Try saying 'open Safari', 'search for weather', or 'create a file'.",
                "actions": ["help_response"],
                "data": {"query": query}
            }
        
        try:
            from api import ai_manager
            
            # Get conversation context
            conversation_summary = ""
            if context.conversation_history:
                recent_exchanges = context.conversation_history[-2:]
                for exchange in recent_exchanges:
                    conversation_summary += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n"
            
            # Query AI
            response = await ai_manager.query_ai(
                prompt=query,
                model=model if model != "auto" else None,
                context=conversation_summary
            )
            
            return {
                "text": response.text,
                "actions": ["ai_response_generated"],
                "data": {
                    "model": response.model,
                    "tokens_used": response.tokens_used,
                    "query": query
                }
            }
            
        except Exception as e:
            self.logger.error(f"AI query error: {e}")
            return {
                "text": f"I'm having trouble processing that request right now, sir. Please try again.",
                "actions": [],
                "data": {"error": str(e)}
            }

class FileOperationsSkill(BaseSkill):
    """File and document operations skill"""
    
    def __init__(self):
        super().__init__(
            name="FileOperations",
            description="Create, read, move, and manage files and folders"
        )
    
    def can_handle(self, intent: Intent) -> bool:
        return intent.name == "file_operations"
    
    async def handle(self, intent: Intent, context: Context) -> Dict[str, Any]:
        """Handle file operations"""
        action = intent.entities.get("action", "").lower()
        target = intent.entities.get("target", "")
        
        self.logger.info(f"File operation: {action} {target}")
        
        try:
            if action in ["create", "make", "new"]:
                return await self._create_file(target)
            elif action in ["read", "open", "show"]:
                return await self._read_file(target)
            elif action in ["delete", "remove"]:
                return await self._delete_file(target)
            else:
                return {
                    "text": f"I'm not sure how to {action} {target}, sir.",
                    "actions": [],
                    "data": {}
                }
                
        except Exception as e:
            self.logger.error(f"File operation error: {e}")
            return {
                "text": f"I encountered an error with that file operation, sir: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _create_file(self, filename: str) -> Dict[str, Any]:
        """Create a new file"""
        try:
            from pathlib import Path
            
            file_path = Path.home() / "Desktop" / filename
            
            if "folder" in filename.lower() or "directory" in filename.lower():
                file_path.mkdir(exist_ok=True)
                return {
                    "text": f"Created folder {filename} on your desktop, sir.",
                    "actions": ["folder_created"],
                    "data": {"path": str(file_path)}
                }
            else:
                file_path.touch()
                return {
                    "text": f"Created file {filename} on your desktop, sir.",
                    "actions": ["file_created"],
                    "data": {"path": str(file_path)}
                }
                
        except Exception as e:
            return {
                "text": f"Error creating {filename}: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _read_file(self, filename: str) -> Dict[str, Any]:
        """Read a file"""
        try:
            from pathlib import Path
            
            # Look in common locations
            possible_paths = [
                Path.home() / "Desktop" / filename,
                Path.home() / "Documents" / filename,
                Path.home() / filename,
                Path(filename)
            ]
            
            for file_path in possible_paths:
                if file_path.exists() and file_path.is_file():
                    content = file_path.read_text()[:500]  # First 500 chars
                    return {
                        "text": f"Here's the content of {filename}:\n\n{content}{'...' if len(content) == 500 else ''}",
                        "actions": ["file_read"],
                        "data": {"path": str(file_path), "content": content}
                    }
            
            return {
                "text": f"I couldn't find the file {filename}, sir.",
                "actions": [],
                "data": {}
            }
            
        except Exception as e:
            return {
                "text": f"Error reading {filename}: {str(e)}",
                "actions": [],
                "data": {"error": str(e)}
            }
    
    async def _delete_file(self, filename: str) -> Dict[str, Any]:
        """Delete a file (with confirmation)"""
        return {
            "text": f"For security, I cannot delete files directly, sir. Please delete {filename} manually if needed.",
            "actions": [],
            "data": {}
        }

class SkillManager:
    """Manages all JARVIS skills"""
    
    def __init__(self):
        self.skills: List[BaseSkill] = []
        self.logger = logging.getLogger("SKILL_MANAGER")
        self.initialize_skills()
    
    def initialize_skills(self):
        """Initialize all available skills"""
        self.skills = [
            SystemControlSkill(),
            WebSearchSkill(),
            AIQuerySkill(),
            FileOperationsSkill()
        ]
        
        self.logger.info(f"✅ Initialized {len(self.skills)} skills")
        for skill in self.skills:
            self.logger.info(f"  - {skill.name}: {skill.description}")
    
    def get_skill_for_intent(self, intent: Intent) -> Optional[BaseSkill]:
        """Get the appropriate skill for an intent"""
        for skill in self.skills:
            if skill.can_handle(intent):
                return skill
        return None
    
    def get_all_skills(self) -> List[BaseSkill]:
        """Get all available skills"""
        return self.skills
    
    def get_help(self) -> str:
        """Get help text for all skills"""
        help_text = "Available JARVIS capabilities:\n\n"
        for skill in self.skills:
            help_text += f"• {skill.get_help()}\n"
        return help_text

# Global skill manager instance
skill_manager = SkillManager()
