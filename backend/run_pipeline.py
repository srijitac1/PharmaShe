import asyncio
import os
import sys

# Add current directory to sys.path to allow imports from 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.research_pipeline import build_pipeline
from app.models.schemas import ResearchState

async def main():
    # Build the LangGraph pipeline
    pipeline = build_pipeline()
    
    # Define initial state
    initial_state = ResearchState(
        biological_focus="Breast Cancer BRCA1",
        evidence=[],
        rrf_score=0.0,
        logs=[]
    )
    
    print("--- Starting Research Pipeline ---")
    
    # Run the pipeline
    result = await pipeline.ainvoke(initial_state)
    
    print("\n--- Pipeline Finished ---")
    print(f"Final RRF Score: {result['rrf_score']}")
    print("\nLogs:")
    for log in result['logs']:
        print(f"- {log}")
    print("\nEvidence Collected:")
    for ev in result['evidence']:
        print(f"- [{ev.source}] {ev.finding} (Rank: {ev.rank})")

if __name__ == "__main__":
    asyncio.run(main())