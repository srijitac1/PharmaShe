from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import random

app = FastAPI()

# Enable CORS to allow requests from the frontend file
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "PharmaShe API System Online"}

@app.get("/api/external/test-integrations")
def test_integrations():
    time.sleep(1)  # Simulate network delay
    return {
        "results": {
            "clinical_trials": {"count": 1245},
            "uspto": {"count": 850},
            "pubmed": {"count": 15200},
            "fda": {"count": 142}
        }
    }

@app.get("/api/reports/generate")
def generate_report():
    time.sleep(1.5)
    return {
        "report_id": f"RPT-{random.randint(1000,9999)}",
        "estimated_completion": "2 minutes"
    }

@app.get("/api/research/query")
def research_query(query: str):
    time.sleep(2)
    # Return dynamic mock data based on query
    market_size = "$12.5 Billion"
    if "breast" in query.lower():
        market_size = "$29.2 Billion"
    
    return {
        "query": query,
        "status": "Completed",
        "agents_involved": ["Master Agent", "Market Analyst", "Patent Scout"],
        "estimated_time": "1.4s",
        "results": {
            "market_analysis": {
                "market_size": market_size,
                "growth_rate": "6.8% CAGR",
                "key_players": ["Roche", "Novartis", "Pfizer", "AstraZeneca"]
            },
            "patent_landscape": {
                "total_patents": 1240,
                "active_patents": 850,
                "expiring_soon": 42
            },
            "clinical_trials": {
                "total_trials": 315,
                "active_trials": 112,
                "recruiting": 45
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)