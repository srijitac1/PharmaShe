import asyncio
import os
import sys
import json
from unittest.mock import MagicMock

# Add the current directory to sys.path to allow imports from 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from app.services.worker_agents.drug_interaction_agent import DrugInteractionAgent
except ImportError as e:
    print(f"Error importing DrugInteractionAgent: {e}")
    print("Make sure you are running this script from the 'backend' directory.")
    sys.exit(1)

async def test_drug_interaction():
    print("--- Testing Drug Interaction Agent ---")
    
    # Initialize Agent
    agent = DrugInteractionAgent()

    # Check if Vertex AI is available in the agent
    if not agent.model:
        print("\n[WARNING] Vertex AI model not initialized.")
        print("Ensure 'google-cloud-aiplatform' is installed and you are authenticated.")
        print("Run: gcloud auth application-default login")
        # We continue anyway to see the fallback response
    else:
        print("[SUCCESS] Vertex AI model initialized.")
    
    # Test Query
    query = "What are the risks of taking Warfarin with Aspirin?"
    print(f"\nProcessing Query: '{query}'")
    
    # Mock DB session (agent signature requires it, but may not use it for this specific task)
    mock_db = MagicMock()
    
    # Execute
    result = await agent.process_query(query, mock_db)
    
    # Output
    print("\n--- Agent Result ---")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_drug_interaction())