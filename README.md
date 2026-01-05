# PharmaShe - Women-Centric Cancer Pharmaceutical Platform

PharmaShe is a forward-looking initiative by a leading multinational generic pharmaceutical company aiming to go beyond the competitive and low-margin generics market. The platform focuses on women's health, especially in cancer care, with the goal of identifying novel, high-value therapies through drug repurposing and indication expansion, integrating RRF Formula (to deal with AI Hallucination) + DeepSomatic Concept (as it is focused on Cancer research) .

## Mission

By leveraging approved molecules in new dosage forms or for underserved patient populations, PharmaShe aims to address unmet clinical needs with differentiated pharmaceutical offerings.

## Agentic AI System

The platform is powered by an Agentic AI system designed to drastically reduce research time and improve decision-making efficiency for product planning and innovation teams by integrating RRF Formula and Google DeepSomatic for minimizing AI Hallucination.

## Key Features

### Core Components

- **Master Agent**: Conversation orchestrator that interprets queries and delegates tasks
- **Worker Agents**: Specialized agents for different research domains
- **Interactive Interface**: Chat-based interface with data visualization
- **Report Generation**: Professional PDF/Excel reports

### Worker Agents

1. **IQVIA Insights Agent**: Market trends, sales data, competitor analysis
2. **EXIM Trends Agent**: Global API and formulation trade data
3. **Patent Landscape Agent**: IP monitoring and freedom-to-operate analysis
4. **Clinical Trials Agent**: Clinical development pipeline monitoring
5. **Internal Knowledge Agent**: Company document analysis
6. **Web Intelligence Agent**: Real-time scientific and regulatory research
7. **Report Generator Agent**: Professional report creation

## Architecture

```
PharmaShe/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── agents/         # AI agent implementations
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── Dockerfile
├── database/               # Database migrations and seeds
├── docker-compose.yml      # Development environment
└── docs/                   # Documentation
```
## Features

- **Intelligent Research**: AI-powered analysis across multiple data sources
- **Market Intelligence**: Real-time market trends and competitor analysis
- **Patent Monitoring**: IP landscape tracking and freedom-to-operate analysis
- **Clinical Pipeline**: Comprehensive trial monitoring and analysis
- **Interactive Reports**: Professional PDF/Excel report generation
- **Chat Interface**: Natural language query processing

## Use Cases

Example queries the system can handle:
- "Which women's cancers show rising incidence but low drug development activity globally?"
- "What are the patent expiration opportunities in breast cancer therapeutics?"
- "Analyze the market potential for repurposing existing oncology drugs for gynecological cancers"
  
<img width="1426" height="755" alt="Screenshot 2026-01-05 at 7 40 23 PM" src="https://github.com/user-attachments/assets/65b90d79-9534-40c9-8eda-d348f7d13ee7" />
<img width="1424" height="799" alt="Screenshot 2026-01-05 at 7 41 16 PM" src="https://github.com/user-attachments/assets/a079b083-90fa-4b94-be52-e81c0f78ba9e" />

## Technology Stack

- **Backend**: FastAPI, PostgreSQL, LangGraph, OpenAI
- **Frontend**: React, TypeScript, Material-UI, Chart.js
- **AI/ML**: LangChain, OpenAI GPT-4, Google Vertex AI (Gemini), Custom Agents
- **Infrastructure**: Docker, Docker Compose
- **APIs**: ClinicalTrials.gov, USPTO, IQVIA (simulated), Google Vertex AI

## License

This project is licensed under the MIT License

---***-------***-------***-------***------

**PharmaShe** - Empowering women's health through intelligent pharmaceutical research.
