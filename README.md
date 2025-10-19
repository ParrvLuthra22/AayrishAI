# 🤖 JARVIS AI Assistant

**Just A Rather Very Intelligent System** - A complete, production-ready AI assistant inspired by Tony Stark's JARVIS.

## ✨ Features

### 🧠 **Advanced Intelligence**
- **Multi-AI Integration**: Groq, OpenAI, Claude, Gemini support
- **Intent Recognition**: Advanced natural language understanding
- **Conversation Memory**: Context-aware interactions
- **Skill-based Architecture**: Modular capability system

### 🎤 **Voice Interaction**
- **Speech Recognition**: "Hey JARVIS" wake word detection
- **Text-to-Speech**: Natural voice responses with voice selection
- **Real-time Processing**: Background voice processing
- **macOS Integration**: Native speech synthesis

### 🖥️ **Modern Interface**
- **PyQt6 GUI**: Futuristic JARVIS-style interface with neon effects
- **Real-time Chat**: Interactive conversation with animated bubbles
- **System Monitoring**: Live CPU, memory, and disk usage
- **Voice Waveforms**: Visual feedback during speech
- **CLI Mode**: Terminal interface for power users

### 🛠️ **System Control**
- **App Management**: Open/close macOS applications
- **System Commands**: Shutdown, restart, sleep, volume control
- **File Operations**: Create, read, and manage files
- **Quick Actions**: One-click buttons for common tasks

### 🌐 **Web Integration**
- **Multi-Engine Search**: DuckDuckGo, Wikipedia, Tavily
- **Real-time Information**: Current news, weather, facts
- **Result Processing**: Intelligent deduplication and formatting

## 🏗️ Clean Architecture

```
JarvisAI/                    # 🎯 Production-ready structure
├── 🧠 core/                 # Intelligence & brain system
│   ├── brain.py            # Intent recognition, conversation memory
│   └── __init__.py         # Core module exports
├── 🎨 ui/                   # User interface components
│   ├── main_window.py      # Primary GUI with JARVIS aesthetics
│   ├── components.py       # Custom widgets (NeonButton, ChatBubble, etc.)
│   └── __init__.py         # UI module exports
├── 🛠️ skills/               # Modular capabilities
│   ├── skill_manager.py    # All 4 core skills integrated
│   └── __init__.py         # Skills module exports
├── 🌐 api/                  # External integrations
│   ├── ai_manager.py       # Multi-AI provider support
│   ├── search_manager.py   # Web search engines
│   └── __init__.py         # API module exports
├── 🎤 system/               # Voice & system control
│   ├── voice_handler.py    # Speech recognition & TTS
│   └── __init__.py         # System module exports
├── ⚙️ config/               # Configuration management
│   ├── settings.py         # Comprehensive config system
│   └── __init__.py         # Config module exports
├── 💾 database/             # Memory & storage
│   ├── memory.py           # Conversation persistence
│   ├── jarvis_memory.db    # SQLite database
│   └── __init__.py         # Database module exports
├── 📝 logs/                 # Activity logging
├── 🚀 main.py              # Main entry point
├── 🛠️ setup.sh             # Automated setup script
├── 🎬 launch.sh            # Quick launcher
├── 📋 Requirements.txt     # Python dependencies
├── 📚 README.md            # This documentation
├── 🎉 BUILD_SUMMARY.md     # Detailed build information
└── 🔐 .env                 # API keys (optional)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS (for full system integration)
- Microphone (for voice commands)

### One-Command Setup
```bash
# Clone and setup everything automatically
git clone <your-repo-url>
cd JarvisAI
./setup.sh
```

### Launch JARVIS
```bash
# GUI Mode (Default) - Futuristic interface
./launch.sh

# CLI Mode - Terminal interface
./launch.sh --cli
```

## 🎯 Usage Examples

### 🎤 Voice Commands (say "Hey JARVIS" first)
```
"Hey JARVIS, open Safari"
"Hey JARVIS, search for Python tutorials"  
"Hey JARVIS, what's the weather like?"
"Hey JARVIS, create a file called notes.txt"
"Hey JARVIS, shut down the system"
"Hey JARVIS, increase volume"
```

### 💬 Text Commands
```
help                    # Show available commands
open spotify           # Launch applications
search machine learning # Web search
what is quantum computing? # AI knowledge queries
create file notes.txt  # File operations
show system info       # Performance metrics
```

### 🖱️ Quick Actions (GUI)
- 🌐 **Search Web** - Instant web search
- 📁 **Open Finder** - File explorer
- 🎵 **Play Music** - Launch music app
- 📧 **Open Mail** - Email client
- 🖥️ **System Info** - Performance metrics

## ⚙️ Configuration

### API Keys (Optional)
```bash
# Add to .env file for enhanced AI features
GROQ_API_KEY=your_groq_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

### Voice Settings
- Wake word customization ("Hey JARVIS")
- Speech rate and volume control
- Voice selection and language
- Microphone sensitivity

### UI Customization  
- JARVIS neon theme with glowing effects
- Animation speed and effects
- Window size and positioning
- Color scheme preferences

## 🎨 JARVIS Interface

### 🖼️ GUI Mode
- **JARVIS Aesthetic**: Neon blue theme (`#00d4ff`) with glowing effects
- **Real-time Chat**: Animated conversation bubbles
- **Voice Waveforms**: Visual feedback during speech recognition
- **System Dashboard**: Live performance monitoring
- **Quick Actions**: One-click common commands
- **Status Bar**: Voice, AI, and connection indicators

### 🖥️ CLI Mode
- **Terminal Interface**: Clean command-line interaction
- **Background Voice**: Continuous listening for wake word
- **Rich Output**: Colored text and status indicators
- **Help System**: Built-in command documentation

## 🔧 Technical Details

### 🎯 Core Components
- **Brain System**: Advanced intent recognition and conversation memory
- **Skill Manager**: 4 integrated skills (System, Web, AI, Files)
- **Voice Handler**: Speech recognition and text-to-speech
- **AI Manager**: Multi-provider integration with fallbacks
- **Search Manager**: Web search across multiple engines

### 📊 Performance
- **Async Architecture**: Non-blocking operations
- **Memory Efficient**: Optimized resource usage  
- **Fast Response**: Sub-second command processing
- **Error Recovery**: Graceful failure handling

### 🛡️ Security
- **Local Processing**: Core operations run on-device
- **API Key Protection**: Environment variable storage
- **System Permissions**: Safe macOS integration
- **Data Encryption**: Secure conversation storage

## 🚨 Troubleshooting

### Common Issues
```bash
# Missing dependencies
pip install -r Requirements.txt

# Voice not working
# Grant microphone permissions in System Preferences

# API errors  
# Add API keys to .env file

# GUI not launching
# Ensure PyQt6 is installed: pip install PyQt6
```

### Debug Information
Check `logs/jarvis_main.log` for detailed error information and system status.

## 🎯 What Makes This Special

### ✨ **Production Ready**
- **2000+ lines** of clean, documented code
- **Modular architecture** for easy extension
- **Comprehensive error handling** and logging
- **Professional UI/UX** with JARVIS aesthetics

### 🤖 **Authentic JARVIS Experience**
- **Voice recognition** with wake word detection
- **Natural speech synthesis** with personality
- **System integration** for real automation
- **Visual effects** inspired by Tony Stark's lab

### 🚀 **Modern Technology**
- **PyQt6** for modern GUI framework
- **Async/await** for responsive performance
- **Multi-AI integration** for intelligent responses
- **Real-time processing** for instant feedback

## 🎬 Demo Scenarios

### Morning Routine
```
User: "Hey JARVIS, good morning"
JARVIS: "Good morning, sir. How may I assist you today?"

User: "Open my email and search for today's weather"
JARVIS: "Opening Mail for you, sir. Searching for current weather information..."
```

### Work Session
```
User: "JARVIS, I need to research machine learning"
JARVIS: "Searching for machine learning information, sir..."
[Shows comprehensive web results]

User: "Create a file called ml-research.txt"
JARVIS: "Created file ml-research.txt on your desktop, sir."
```

## 🤝 Contributing

This is a complete, production-ready system. Feel free to:
- Add new skills to the skill manager
- Integrate additional AI providers
- Enhance the UI with new components
- Add platform support (Windows/Linux)

## 📝 License

MIT License - Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Marvel/Disney**: Inspiration from Iron Man's JARVIS
- **PyQt6**: Modern GUI framework
- **Groq**: Lightning-fast AI inference
- **Open Source Community**: Amazing tools and libraries

---

### 🎬 *"I am JARVIS, sir. At your service."*

**JARVIS AI Assistant - Your personal AI companion, ready to assist with anything you need.** 🚀

**Built with ❤️ and inspired by the future Tony Stark envisioned.**
