import os
import vertexai
from vertexai.generative_models import GenerativeModel

# Configuration for Project: gen-lang-client-0786690668
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0786690668")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

def init_vertex_ai():
    """Initializes the Vertex AI SDK with the specific project."""
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def get_gemini_model(model_name: str = "gemini-1.5-flash") -> GenerativeModel:
    """
    Returns a configured GenerativeModel instance connected to the project.
    """
    init_vertex_ai()
    return GenerativeModel(model_name)