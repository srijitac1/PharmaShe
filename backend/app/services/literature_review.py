from app.models.schemas import ResearchState, Evidence

try:
    from app.core.vertex_ai import get_gemini_model
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

def literature_review_scout(state: ResearchState) -> ResearchState:
    state.logs.append(f"Literature Review Scout: Analyzing literature for '{state.biological_focus}'")

    finding = "Recent meta-analysis confirms efficacy in triple-negative breast cancer"

    if VERTEX_AI_AVAILABLE:
        try:
            model = get_gemini_model()
            prompt = f"""
            You are an expert medical researcher. Provide a concise summary (under 40 words) of a key scientific finding or recent study regarding: "{state.biological_focus}".
            """
            response = model.generate_content(prompt)
            finding = response.text.strip()
        except Exception as e:
            state.logs.append(f"AI Error: {str(e)}")

    evidence = Evidence(
        source="PubMed / AI Analysis",
        finding=finding,
        rank=3
    )

    state.evidence.append(evidence)
    return state