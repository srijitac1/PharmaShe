from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.services.external_apis import ExternalAPIService

router = APIRouter()

@router.get("/test-integrations")
async def test_external_integrations():
    """
    Test all external API integrations
    """
    try:
        api_service = ExternalAPIService()
        
        # Test each API individually
        results = {}
        
        # Test Clinical Trials API
        try:
            trials_data = await api_service.clinical_trials_api.search_trials(
                condition="breast cancer",
                limit=5
            )
            results["clinical_trials"] = {
                "status": "success",
                "count": len(trials_data.get("trials", [])),
                "sample_trial": trials_data.get("trials", [{}])[0] if trials_data.get("trials") else None
            }
        except Exception as e:
            results["clinical_trials"] = {"status": "error", "error": str(e)}
        
        # Test USPTO API
        try:
            patents_data = await api_service.uspto_api.search_patents(
                query="cancer treatment",
                limit=5
            )
            results["uspto"] = {
                "status": "success",
                "count": len(patents_data.get("patents", [])),
                "sample_patent": patents_data.get("patents", [{}])[0] if patents_data.get("patents") else None
            }
        except Exception as e:
            results["uspto"] = {"status": "error", "error": str(e)}
        
        # Test PubMed API
        try:
            articles_data = await api_service.pubmed_api.search_articles(
                query="breast cancer",
                max_results=5
            )
            results["pubmed"] = {
                "status": "success",
                "count": len(articles_data.get("articles", [])),
                "sample_article": articles_data.get("articles", [{}])[0] if articles_data.get("articles") else None
            }
        except Exception as e:
            results["pubmed"] = {"status": "error", "error": str(e)}
        
        # Test FDA API
        try:
            fda_data = await api_service.fda_api.search_drugs(
                search_term="cancer",
                limit=5
            )
            results["fda"] = {
                "status": "success",
                "count": len(fda_data.get("drugs", [])),
                "sample_drug": fda_data.get("drugs", [{}])[0] if fda_data.get("drugs") else None
            }
        except Exception as e:
            results["fda"] = {"status": "error", "error": str(e)}
        
        await api_service.close()
        
        return {
            "message": "External API integration test completed",
            "results": results,
            "timestamp": "2024-01-25T15:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Integration test failed: {str(e)}")

@router.get("/comprehensive-search")
async def comprehensive_search(
    query: str = Query(..., description="Search query"),
    therapeutic_area: Optional[str] = Query(None, description="Therapeutic area filter"),
    drug_name: Optional[str] = Query(None, description="Drug name filter"),
    db: Session = Depends(get_db)
):
    """
    Perform comprehensive search across all external APIs
    """
    try:
        api_service = ExternalAPIService()
        
        comprehensive_data = await api_service.search_comprehensive_research(
            query=query,
            therapeutic_area=therapeutic_area,
            drug_name=drug_name
        )
        
        await api_service.close()
        
        return comprehensive_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market-intelligence")
async def get_market_intelligence(
    therapeutic_area: str = Query(..., description="Therapeutic area"),
    drug_name: Optional[str] = Query(None, description="Drug name"),
    db: Session = Depends(get_db)
):
    """
    Get market intelligence for a specific therapeutic area
    """
    try:
        api_service = ExternalAPIService()
        
        market_data = await api_service.get_market_intelligence(
            therapeutic_area=therapeutic_area,
            drug_name=drug_name
        )
        
        await api_service.close()
        
        return market_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/competitive-landscape")
async def get_competitive_landscape(
    therapeutic_area: str = Query(..., description="Therapeutic area"),
    drug_name: Optional[str] = Query(None, description="Drug name"),
    db: Session = Depends(get_db)
):
    """
    Get competitive landscape analysis
    """
    try:
        api_service = ExternalAPIService()
        
        competitive_data = await api_service.get_competitive_landscape(
            therapeutic_area=therapeutic_area,
            drug_name=drug_name
        )
        
        await api_service.close()
        
        return competitive_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
