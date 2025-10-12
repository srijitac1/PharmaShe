# PharmaShe - Women-Centric Cancer Pharmaceutical Platform

PharmaShe is a forward-looking initiative by a leading multinational generic pharmaceutical company aiming to go beyond the competitive and low-margin generics market. The platform focuses on women's health, especially in cancer care, with the goal of identifying novel, high-value therapies through drug repurposing and indication expansion.

## Mission

By leveraging approved molecules in new dosage forms or for underserved patient populations, PharmaShe aims to address unmet clinical needs with differentiated pharmaceutical offerings.

## 🤖 Agentic AI System

The platform is powered by an Agentic AI system designed to drastically reduce research time and improve decision-making efficiency for product planning and innovation teams.

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

##  Architecture

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



1. **Clone and setup**:
   ```bash
   git clone https://github.com/srijitac1/PharmaShe.git
   cd PharmaShe
   ```

2. **Start with Docker**:
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm start
```

# Features

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

## Technology Stack

- **Backend**: FastAPI, PostgreSQL, LangGraph, OpenAI
- **Frontend**: React, TypeScript, Material-UI, Chart.js
- **AI/ML**: LangChain, OpenAI GPT-4, Custom Agents
- **Infrastructure**: Docker, Docker Compose
- **APIs**: ClinicalTrials.gov, USPTO, IQVIA (simulated)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- FastAPI for the backend framework
- React and Material-UI for the frontend
- All contributors and testers


---

**PharmaShe** - Empowering women's health through intelligent pharmaceutical research.