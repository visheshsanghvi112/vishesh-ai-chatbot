# Enhanced Vishesh GPT Chatbot

An intelligent AI chatbot powered by Google Gemini 1.5 Flash with full conversation memory.

## 🚀 Features

- **Full Conversation Memory**: Remembers all messages in current session
- **ChatGPT-like Intelligence**: Natural, context-aware responses
- **Data Analysis**: Upload CSV/Excel files for analysis
- **Smart Commands**: Built-in commands for quick actions
- **Secure API Key Management**: Environment variable support

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

**Option A: For Local Development**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

**Option B: For Streamlit Cloud**

1. Deploy your app to Streamlit Cloud
2. Go to app settings → Secrets
3. Add:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

**Option C: Environment Variable**

PowerShell:
```powershell
$env:GEMINI_API_KEY="your-actual-api-key-here"
```

### 3. Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste it into your configuration

### 4. Run the Chatbot

```bash
streamlit run test.py
```

## 📝 Available Commands

- `/help` - Show all available commands
- `/clear` - Clear conversation history
- `/memory` - Show conversation memory info
- `/date` - Get current date/time
- `/creator` - About the creator
- `/analyze` - Analyze uploaded data
- `/stats` - Get data statistics
- `/export` - Export chat history

## 🎯 Usage Tips

1. **Natural Conversations**: Just chat naturally - the AI remembers everything
2. **Follow-up Questions**: Ask follow-ups without repeating context
3. **Data Analysis**: Upload CSV/Excel files in the sidebar
4. **Commands**: Use `/help` anytime to see available commands

## 🛠️ Technical Details

- **AI Model**: Google Gemini 1.5 Flash
- **Framework**: Streamlit
- **Context Window**: Last 30 messages
- **Max Output**: 4096 tokens
- **Temperature**: 0.9 (creative responses)

## 👨‍💻 Creator

Created by **Vishesh Sanghvi**

Connect: [LinkedIn](https://www.linkedin.com/in/vishesh-sanghvi-96b16a237/)

## 🔒 Security Note

- Never commit your API key to GitHub
- Use `.streamlit/secrets.toml` (already in .gitignore)
- Or use environment variables
- Rotate keys regularly

## 📦 Dependencies

See `requirements.txt` for full list. Key packages:
- `streamlit` - Web interface
- `requests` - API calls
- `pandas` - Data analysis
- `plotly` - Visualizations

---

Built with ❤️ using Google Gemini AI
