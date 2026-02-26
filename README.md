🎬 Agentic-AI-Based-Video-Creator

An autonomous, zero-budget AI system that generates, critiques, optimizes, renders, and prepares YouTube Shorts videos end-to-end using a multi-agent architecture.

Built with structured LLM outputs, deterministic validation, and a modular media pipeline.

🚀 Features

✅ Multi-agent AI architecture
✅ Structured JSON outputs (Pydantic enforced)
✅ Script generation with multiple variations
✅ Self-critique + debate-based selection
✅ Hook optimization (Retention Agent)
✅ SEO metadata generation
✅ Thumbnail concept generation
✅ Image generation (API or local diffusion)
✅ Text-to-Speech (Piper / local)
✅ Automated video rendering (FFmpeg)
✅ Analytics logging
✅ Fully zero-budget compatible

🧠 Architecture Overview
Planner
↓
Research
↓
Multiple Script Variations
↓
Critic Agents
↓
Debate Selection
↓
Retention Optimization
↓
SEO + Thumbnail Agents
↓
Media Pipeline (Images + TTS + Video)
↓
Upload + Analytics
📁 Project Structure
Agentic-AI-Based-Video-Creator/

├── agents/
│ ├── base_agent.py
│ ├── planner_agent.py
│ ├── research_agent.py
│ ├── script_agent.py
│ ├── critic_agent.py
│ ├── debate_critic_agent.py
│ ├── retention_agent.py
│ ├── seo_agent.py
│ └── thumbnail_agent.py
│
├── media_pipeline/
│ ├── image_generator.py
│ ├── tts_engine.py
│ ├── video_renderer.py
│ └── thumbnail_renderer.py
│
├── orchestrator/
│ ├── engine.py
│ └── memory.py
│
├── analytics/
│ └── performance_tracker.py
│
├── models/
│ └── schemas.py
│
├── utils/
│ └── llm.py
│
└── main.py
⚙️ Requirements

Python 3.10+ (Recommended)

Ollama (for local LLM)

FFmpeg

Pillow

Requests

Optional:

Stable Diffusion / API service

Piper TTS

YouTube API credentials

📦 Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/Agentic-AI-Based-Video-Creator.git
cd Agentic-AI-Based-Video-Creator
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate # Windows
3️⃣ Install dependencies
pip install -r requirements.txt

If no requirements file:

pip install pydantic requests pillow google-api-python-client
🧠 LLM Setup (Ollama)

Install Ollama:
https://ollama.com/

Pull model:

ollama pull qwen2.5:7b

Ensure utils/llm.py is configured correctly.

🎨 Image Generation Options

You can use:

Stable Horde (free API)

DeepAI API

Replicate

Local Diffusers

ComfyUI

Automatic1111

Update media_pipeline/image_generator.py accordingly.

🔊 TTS Setup (Piper Recommended)

Download Piper:
https://github.com/rhasspy/piper/releases

Place:

piper.exe
voice_model.onnx

Update path inside tts_engine.py.

🎬 Run the System
python main.py

The system will:

Generate topic

Create scripts

Self-evaluate

Optimize hook

Generate SEO + thumbnail

Generate images

Generate voice

Render final video

Save metadata

Output folder:

/output/
📊 Analytics Logging

Each generated video logs:

Topic

Title

Paths

Timestamp

Stored in:

analytics_log.json
🧠 Design Principles

LLM handles creativity

Python handles validation

Structured outputs enforced via Pydantic

Deterministic approval logic

Agent-based modularity

Zero-budget friendly

🔥 Why Agentic Architecture?

Instead of a single prompt pipeline:

This system:

Generates multiple competing scripts

Uses critics for scoring

Uses debate to select winner

Improves retention hooks

Separates creativity from enforcement

This increases output quality and reliability.

📈 Future Improvements

YouTube auto-upload integration

Performance-based feedback loop

Multi-channel scaling

Trend-based topic generation

Vector memory storage

Distributed execution

⚠ Disclaimer

This tool is for educational and experimental use.

Ensure compliance with:

YouTube policies

Copyright rules

API usage limits

🏆 Project Goal

To demonstrate a fully autonomous AI content pipeline using:

Multi-agent reasoning

Structured LLM outputs

Deterministic validation

Zero-cost infrastructure

👨‍💻 Author

Built as an experimental autonomous AI media system.
