# 🤖 AI-Powered Blog Generator from YouTube Videos

An intelligent multi-agent system built with **CrewAI** that automatically generates blog posts by researching and analyzing YouTube video content. This project uses **Groq's LLM** for agent reasoning and **HuggingFace embeddings** for semantic search, making it completely free to use without OpenAI dependencies.

## ✨ Features

- 🎥 **YouTube Channel Analysis**: Automatically processes and indexes entire YouTube channels
- 🤖 **Multi-Agent System**: Coordinated AI agents for research and content creation
- 📝 **Automated Blog Writing**: Generates well-structured blog posts from video transcripts
- 🔍 **Semantic Search**: Uses HuggingFace embeddings for intelligent video content retrieval
- 💾 **Local Caching**: Stores processed videos locally to avoid reprocessing
- 🆓 **No OpenAI Required**: Uses Groq's free LLM API and open-source embeddings
- ⚡ **Fast & Efficient**: Leverages Groq's lightning-fast inference

## 🏗️ Architecture

The system consists of two specialized AI agents:

1. **Blog Researcher Agent**: Searches through YouTube channel content and extracts relevant information
2. **Blog Writer Agent**: Creates engaging, well-structured blog posts from the research

## 🛠️ Tech Stack

- **[CrewAI](https://github.com/joaomdmoura/crewAI)**: Multi-agent orchestration framework
- **[Groq](https://groq.com/)**: Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **[HuggingFace](https://huggingface.co/)**: Local embeddings (sentence-transformers)
- **[Embedchain](https://embedchain.ai/)**: Vector database and RAG framework
- **Python 3.10+**: Core programming language

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher installed
- A Groq API key (free tier available)
- Git for version control

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Crew-AI-YT_Video
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Get your free Groq API key:**
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key

## 📁 Project Structure

```
Crew-AI-YT_Video/
├── agents.py           # AI agent definitions (researcher & writer)
├── tasks.py            # Task definitions for agents
├── tools.py            # YouTube search tool configuration
├── crew.py             # Main orchestration and execution
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (API keys)
├── .gitignore          # Git ignore patterns
├── db/                 # Local vector database (auto-generated)
│   └── chroma.sqlite3  # Cached video embeddings
└── new-blog-post.md    # Generated blog output
```

## 🎯 Usage

### Basic Usage

Run the blog generator with default settings:

```bash
python crew.py
```

This will:
1. Process videos from the configured YouTube channel
2. Research the specified topic
3. Generate a blog post saved to `new-blog-post.md`

### Customize the Topic

Edit `crew.py` to change the research topic:

```python
result = crew.kickoff(inputs={'topic': 'Your Topic Here'})
```

### Change YouTube Channel

Edit `tools.py` to target a different channel:

```python
yt_tool = YoutubeChannelSearchTool(
    youtube_channel_handle='@YourChannelHandle',
    config=config
)
```

### Adjust Output Length

Modify `tasks.py` to control blog length:

```python
expected_output='Summarize the info... in 500 words'  # Change word count
```

## 🔧 Configuration

### Agent Configuration (`agents.py`)

- **Model Selection**: Change the LLM model in the `llm` configuration
- **Agent Behavior**: Modify `role`, `goal`, and `backstory` for different writing styles
- **Memory**: Currently disabled to avoid OpenAI dependency (can be re-enabled with custom embeddings)

### Task Configuration (`tasks.py`)

- **Research Depth**: Adjust `expected_output` for more/less detailed research
- **Output Format**: Customize the blog post structure and length

### Tool Configuration (`tools.py`)

- **Embedding Model**: Change the HuggingFace model for different performance/quality trade-offs
- **YouTube Channel**: Target different content sources

## 🤔 How It Works

### Step 1: Video Processing
When you first run the script, it:
- Fetches all videos from the specified YouTube channel
- Downloads and processes video transcripts
- Creates embeddings using HuggingFace's sentence-transformers
- Stores everything in a local SQLite database (`db/chroma.sqlite3`)

**Note**: First run takes 15-20 minutes for large channels. Subsequent runs use cached data!

### Step 2: Research Phase
The **Blog Researcher Agent**:
- Receives your topic query
- Searches the vector database for relevant video content
- Extracts key information and insights
- Compiles a comprehensive research report

### Step 3: Writing Phase
The **Blog Writer Agent**:
- Takes the research report
- Crafts an engaging, well-structured blog post
- Simplifies complex technical concepts
- Outputs the final blog to `new-blog-post.md`

## 🎨 Customization Ideas

- **Multi-Channel Analysis**: Modify to compare content across multiple channels
- **SEO Optimization**: Add an SEO specialist agent to optimize blog posts
- **Social Media Posts**: Create agents to generate Twitter threads or LinkedIn posts
- **Video Summaries**: Generate video summaries instead of full blog posts
- **Podcast Transcripts**: Adapt for podcast content analysis

## ⚠️ Troubleshooting

### Rate Limit Errors (Groq)

**Error**: `RateLimitError: Request too large for model`

**Solution**: 
- Switch to `llama-3.1-8b-instant` for higher rate limits (30K TPM)
- Reduce output length in `tasks.py`
- Make task descriptions more specific

### First Run Taking Too Long

**Cause**: Processing all channel videos for the first time

**Solution**: 
- Be patient! This is a one-time operation
- Database caching makes subsequent runs instant
- Consider testing with a smaller channel first

### Import Errors

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

## 📊 Performance

- **First Run**: 15-20 minutes (for ~1700 videos)
- **Subsequent Runs**: 2-5 minutes (cached)
- **Database Size**: ~170 KB for 1700 videos
- **Embedding Model**: ~90 MB (one-time download)

## 🔐 Security

- ✅ `.env` file excluded from Git
- ✅ API keys never committed to repository
- ✅ Database cached locally (not shared)
- ✅ All processing happens on your machine

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [Groq](https://groq.com/) - Lightning-fast LLM inference
- [HuggingFace](https://huggingface.co/) - Open-source embeddings
- [Embedchain](https://embedchain.ai/) - RAG framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing GitHub Issues
3. Create a new issue with detailed information

---

**Built with ❤️ using CrewAI and Groq**

*Happy Blogging! 📝✨*