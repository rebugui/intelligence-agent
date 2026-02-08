# Intelligence Agent

> AI-powered security news collection and technical blog writing automation system

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Intelligence Agent is an automated AI system that:
- Collects security and technology news from multiple sources
- Evaluates article quality using AI scoring
- Writes in-depth technical blog posts with multiple personas
- Publishes to Notion for human review
- Automatically deploys to Hugo-powered blogs

## Architecture

```
News Collector → AI Selector → AI Writer → Notion → Git Publisher → Hugo Blog
```

### Key Components

- **Collector**: Multi-source news aggregation (Google News, arXiv, HackerNews, Hada.io)
- **Selector**: AI-based quality scoring (1-10 scale, threshold 6+)
- **Writer**: Multi-persona blog generation with Mermaid diagrams
- **Publisher**: Notion integration + Git automation

## Features

- ✅ Async parallel processing (3-5x faster)
- ✅ Multi-persona writing (Security Expert, AI Researcher, DevOps Engineer, CVE Analyst)
- ✅ Mermaid diagram pipeline (AI Writer → Notion → Git → Hugo)
- ✅ 2-stage AI generation (metadata + content separation)
- ✅ Automatic code splitting (Notion 2000 char limit)
- ✅ Natural boundary code splitting for readability

## Installation

```bash
# Clone repository
git clone https://github.com/rebugui/intelligence-agent.git
cd intelligence-agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Required environment variables:

```bash
# Notion
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id

# ZhipuAI (LLM)
GLM_API_KEY=your_glm_api_key
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
GLM_MODEL=glm-4

# Git
BLOG_REPO_PATH=/path/to/your/blog
BLOG_URL=https://your-blog-url.com/
```

## Usage

### Run Pipeline

```bash
# Collect news, evaluate, and write blog posts
python -m src.intelligence_pipeline --max-articles 5
```

### Git Publisher

```bash
# Publish reviewed articles from Notion to Git
python src/run_git_publisher.py
```

### Development

```bash
# Test full pipeline
python src/test_full_pipeline.py

# Test Mermaid conversion
python src/test_mermaid_fix.py
```

## Project Structure

```
intelligence-agent/
├── src/                    # Core Python modules
│   ├── collector.py        # News collection
│   ├── selector.py         # AI-based article selection
│   ├── writer.py           # Multi-persona blog writing
│   ├── notion_publisher.py # Notion integration
│   ├── publisher_git.py    # Git automation
│   └── intelligence_pipeline.py # Main pipeline
├── config/
│   └── prompts.yaml        # AI system prompts
├── tests/                  # Test files
├── docs/                   # Documentation
└── requirements.txt        # Python dependencies
```

## AI Personas

The system uses 4 specialized personas:

1. **Security Expert**: CVE analysis, attack scenarios, PoC code
2. **AI/ML Researcher**: Paper analysis, architecture diagrams
3. **DevOps Engineer**: Practical guides, configuration examples
4. **CVE Analyst**: CVSS vectors, impact assessment

## Mermaid Diagram Pipeline

1. AI Writer generates ```mermaid blocks
2. Notion Publisher converts to javascript code blocks
3. Git Publisher restores to ```mermaid
4. Hugo renders with auto dark/light theme

## Performance

| Metric | Result |
|:---|:---|
| Collection Success Rate | 100% |
| AI Selection Pass Rate | 6% (quality threshold) |
| Writing Success Rate | 99% (2-stage separation) |
| Publishing Success Rate | 100% |

## Documentation

- [Technical Report](docs/Intelligence_agent_REPORT.md)
- [Architecture](docs/README.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**rebugui** - [GitHub](https://github.com/rebugui)

## Acknowledgments

- ZhipuAI GLM-4 for powerful LLM capabilities
- Notion for excellent content management
- Hugo for fast static site generation
