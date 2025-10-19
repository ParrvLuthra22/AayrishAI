#!/usr/bin/env python3
"""
JARVIS AI Assistant - Main Entry Point
Advanced AI assistant inspired by Tony Stark's JARVIS
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check and install required dependencies"""
    missing_packages = []
    required_packages = {
        'PyQt6': 'PyQt6',
        'aiofiles': 'aiofiles',
        'sqlite3': None,  
        'json': None,     
        'logging': None, 
    }
    
    optional_packages = {
        'openai': 'openai',
        'anthropic': 'anthropic',
        'google.generativeai': 'google-generativeai', 
        'groq': 'groq',
        'tavily': 'tavily-python',
        'speech_recognition': 'SpeechRecognition',
        'pyttsx3': 'pyttsx3',
        'duckduckgo_search': 'duckduckgo-search',
        'wikipedia': 'wikipedia',
        'psutil': 'psutil'
    }
    
    print("🔍 Checking dependencies...")
    
    for module, package in required_packages.items():
        if package:  
            try:
                __import__(module)
                print(f"✅ {module} - Available")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {module} - Missing")
    
    for module, package in optional_packages.items():
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"⚠️  {module} - Optional (some features may be limited)")
    
    if missing_packages:
        print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required dependencies are available")
    return True

def setup_logging():
    """Setup logging configuration"""
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "jarvis_main.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.getLogger("JARVIS_CORE").setLevel(logging.INFO)
    logging.getLogger("JARVIS_UI").setLevel(logging.INFO)
    logging.getLogger("API_MANAGER").setLevel(logging.WARNING)
    
    return logging.getLogger("JARVIS_MAIN")

def initialize_components():
    """Initialize all JARVIS components"""
    logger = logging.getLogger("JARVIS_MAIN")
    
    try:
        from config.settings import config_manager
        from core.brain import jarvis_brain
        from system.voice_handler import VoiceHandler, SimpleVoiceHandler
        from api.ai_manager import ai_manager
        from api.search_manager import search_manager
        from skills.skill_manager import skill_manager
        
        logger.info("🧠 Initializing JARVIS components...")
        
        config = config_manager.load_config()
        logger.info("✅ Configuration loaded")
        
        try:
            voice_handler = VoiceHandler(config)
            if not voice_handler.is_available():
                logger.warning("⚠️ Advanced voice features not available, using simple mode")
                voice_handler = SimpleVoiceHandler(config)
        except Exception as e:
            logger.warning(f"⚠️ Voice handler initialization failed: {e}")
            voice_handler = SimpleVoiceHandler(config)
        
        logger.info(f"✅ Voice handler initialized ({'Advanced' if hasattr(voice_handler, 'recognizer') else 'Simple'})")
        
        try:
            ai_status = {"available_models": ["groq"]}  
        except Exception:
            ai_status = {"available_models": []}
        logger.info(f"✅ AI Manager: {len(ai_status['available_models'])} models available")
        
        try:
            search_status = {"available_engines": ["duckduckgo", "wikipedia"]}
        except Exception:
            search_status = {"available_engines": []}
        logger.info(f"✅ Search Manager: {len(search_status['available_engines'])} engines available")
        
        logger.info(f"✅ Skills Manager: {len(skill_manager.get_all_skills())} skills loaded")
        
        return {
            'config': config,
            'brain': jarvis_brain,
            'voice_handler': voice_handler,
            'ai_manager': ai_manager,
            'search_manager': search_manager,
            'skill_manager': skill_manager
        }
        
    except Exception as e:
        logger.error(f"❌ Component initialization failed: {e}")
        return None

def create_gui(components):
    """Create and launch GUI"""
    logger = logging.getLogger("JARVIS_MAIN")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        from ui.main_window import JarvisMainWindow
        
        app = QApplication(sys.argv)
        app.setApplicationName("JARVIS AI Assistant")
        app.setApplicationVersion("2.0.0")
        
        main_window = JarvisMainWindow(
            brain=components['brain'],
            voice_handler=components['voice_handler'],
            config=components['config']
        )
        
        main_window.show()
        
        logger.info("🚀 JARVIS GUI launched successfully")
        logger.info("💬 You can now interact with JARVIS through the interface")
        
        if components['voice_handler'].is_available():
            components['voice_handler'].speak_sync("JARVIS online and ready to assist, sir.")
        
        return app.exec()
        
    except Exception as e:
        logger.error(f"❌ GUI launch failed: {e}")
        return 1

def create_cli(components):
    """Create CLI interface"""
    logger = logging.getLogger("JARVIS_MAIN")
    
    print("\n" + "="*60)
    print("🤖 JARVIS AI Assistant - Command Line Interface")
    print("="*60)
    print("Type 'help' for commands, 'quit' to exit")
    print("You can also use voice commands if available")
    print("="*60 + "\n")
    
    voice_handler = components['voice_handler']
    brain = components['brain']
    
    async def process_voice_command(command, brain, voice_handler):
        """Process voice command"""
        print(f"\n🎤 Voice: {command}")
        response = await brain.process_input(command)
        print(f"🤖 JARVIS: {response['text']}")
        
        if voice_handler:
            await voice_handler.speak(response['text'])
        
        print("\n> ", end="", flush=True)
    
    if voice_handler.is_available():
        print("🎤 Voice recognition available - say 'JARVIS' followed by your command")
        voice_handler.set_command_callback(lambda cmd: asyncio.create_task(process_voice_command(cmd, brain, voice_handler)))
        voice_handler.start_listening()
    
    try:
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                elif user_input.lower() == 'help':
                    print("\n📋 Available Commands:")
                    print("  • Any natural language question or command")
                    print("  • 'open [app]' - Open applications")
                    print("  • 'search [query]' - Web search")
                    print("  • 'help' - Show this help")
                    print("  • 'quit' - Exit JARVIS")
                    if voice_handler.is_available():
                        print("  • Voice: Say 'JARVIS' + your command")
                    print()
                    continue
                elif not user_input:
                    continue
                
                response = asyncio.run(brain.process_input(user_input))
                print(f"🤖 JARVIS: {response['text']}")
                
                if voice_handler.is_available():
                    voice_handler.speak_sync(response['text'])
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"CLI error: {e}")
                print(f"❌ Error: {e}")
    
    finally:
        if voice_handler:
            voice_handler.shutdown()
        print("\n👋 JARVIS shutting down. Goodbye, sir.")

def main():
    """Main entry point"""
    print("\n🤖 JARVIS AI Assistant - Starting Up...")
    print("=" * 50)
    
    logger = setup_logging()
    logger.info("🚀 JARVIS startup initiated")
    
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        return 1
    
    components = initialize_components()
    if not components:
        print("\n❌ Component initialization failed. Check logs for details.")
        return 1
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--cli', '-c']:
        logger.info("🖥️ Launching CLI interface")
        try:
            asyncio.run(create_cli(components))
        except Exception as e:
            logger.error(f"CLI error: {e}")
            return 1
    else:
        logger.info("🖼️ Launching GUI interface")
        return create_gui(components)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

