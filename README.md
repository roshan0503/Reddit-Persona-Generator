# Reddit User Persona Generator

A powerful Python tool that analyzes Reddit user profiles and generates comprehensive personas using Groq's Llama3 AI models. This tool scrapes user posts and comments to create detailed psychological profiles with evidence-based insights.

## 🚀 Features

- **AI-Powered Analysis**: Uses Groq's ultra-fast Llama3 models for deep persona generation
- **Comprehensive Profiling**: Analyzes interests, personality traits, writing style, values, and Reddit behavior
- **Evidence-Based**: All insights are backed by specific quotes and post/comment citations
- **Dual Interface**: Both web-based (Streamlit) and command-line interfaces
- **Fast Processing**: Leverages Groq's infrastructure for lightning-fast results
- **File Export**: Saves personas as downloadable text files

## 📋 Requirements

- Python 3.7+
- Reddit API access (already configured)
- Groq API access (already configured)

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
```

2. **Install required dependencies:**
```bash
pip install praw groq streamlit requests argparse
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### Option 1: Web Interface (Recommended)

1. **Launch the Streamlit app:**
```bash
streamlit run reddit_persona.py
```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Enter a Reddit profile URL** (e.g., `https://www.reddit.com/user/username/`)

4. **Configure settings** (optional):
   - Content limit (10-500 posts/comments)
   - Model selection (llama3-70b-8192 recommended)

5. **Click "Generate Persona"** and wait for results

6. **Download the generated persona** as a text file

### Option 2: Command Line Interface

**Basic usage:**
```bash
python reddit_persona.py --url https://www.reddit.com/user/username/
```

**Advanced usage with options:**
```bash
python reddit_persona.py --url https://www.reddit.com/user/username/ --limit 200 --model llama3-8b-8192
```

## 📊 Available Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `llama3-70b-8192` | Best quality, most detailed analysis | **Recommended** for comprehensive personas |
| `llama3-8b-8192` | Fastest processing, good quality | Quick analysis or testing |
| `mixtral-8x7b-32768` | Balanced speed and quality | General purpose |

## 💡 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Reddit profile URL (required) | - |
| `--limit` | Max posts/comments to analyze | 100 |
| `--model` | Groq model to use | llama3-70b-8192 |

## 📁 Output Structure

Generated personas are saved in the `output/` directory with the following structure:

```
output/
├── username1_persona.txt
├── username2_persona.txt
└── ...
```

Each persona file contains:
- **Interests/Hobbies** with evidence
- **Personality Traits** with citations
- **Writing Style/Tone** analysis
- **Values/Beliefs** identification
- **Reddit Behavior** patterns
- **Generation timestamp**

## 🔍 Sample Personas

The repository includes sample persona files for demonstration:

- `sample_user1_persona.txt` - Tech enthusiast profile
- `sample_user2_persona.txt` - Creative writer profile
- `sample_user3_persona.txt` - Gaming community member

## 🛠️ Configuration

### API Credentials
The tool comes pre-configured with API credentials:
- **Reddit API**: Already set up for immediate use
- **Groq API**: Connected to high-performance Llama3 models

### Customization Options

**Modify content limits:**
```python
# In the script, adjust default values
scrape_limit = 200  # Increase for more comprehensive analysis
```

**Change default model:**
```python
# In PersonaGenerator class
self.model = "llama3-8b-8192"  # For faster processing
```

## 📖 Usage Examples

### Example 1: Basic Analysis
```bash
python reddit_persona.py --url https://www.reddit.com/user/spez/
```

### Example 2: Deep Analysis
```bash
python reddit_persona.py --url https://www.reddit.com/user/spez/ --limit 300 --model llama3-70b-8192
```

### Example 3: Quick Test
```bash
python reddit_persona.py --url https://www.reddit.com/user/spez/ --limit 50 --model llama3-8b-8192
```

## 🎨 Web Interface Features

- **Real-time progress tracking**
- **Interactive model selection**
- **Adjustable content limits**
- **One-click download**
- **Analysis statistics**
- **Error handling and validation**

## 🔒 Privacy & Ethics

- **No data storage**: User data is processed in real-time and not stored
- **Public data only**: Only analyzes publicly available Reddit content
- **Ethical usage**: Designed for legitimate research and analysis purposes
- **Rate limiting**: Respects Reddit's API guidelines

## 🐛 Troubleshooting

### Common Issues

**1. "User not found" error:**
- Verify the Reddit username is spelled correctly
- Check if the user account is suspended or deleted
- Ensure the profile URL format is correct

**2. "No content found" error:**
- User may have no public posts/comments
- Try increasing the content limit
- Check if the account is very new

**3. API rate limiting:**
- Wait a few minutes before trying again
- Reduce the content limit temporarily
- The tool respects API rate limits automatically

**4. Installation issues:**
```bash
# If you encounter permission errors
pip install --user praw groq streamlit requests argparse

# If you have Python version conflicts
python3 -m pip install praw groq streamlit requests argparse
```

## 📊 Performance

- **Processing time**: 10-30 seconds per user (depending on content volume)
- **Content limit**: Up to 500 posts/comments per analysis
- **Accuracy**: High-quality insights with evidence-based citations
- **Speed**: Ultra-fast with Groq's optimized infrastructure

## 🔄 Updates & Maintenance

To update the tool:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the sample personas for expected output format

## 🙏 Acknowledgments

- **Reddit API** for providing access to user data
- **Groq** for ultra-fast AI inference
- **Llama3** for high-quality language understanding
- **Streamlit** for the intuitive web interface

---

**⚡ Ready to analyze Reddit personas? Start with the web interface for the best experience!**

```bash
streamlit run reddit_persona.py
```
