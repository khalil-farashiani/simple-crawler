from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..celery.task import fetch_filtered_data

router = APIRouter()



class FilterParams(BaseModel):
    visas: List[str] 


@router.get("/ocupations")
async def create_crawl_task(filters: FilterParams):
    try:
        for visa in filters.visas:
            result = fetch_filtered_data.delay(visa)
            print(f"Task initiated for visa {visa}, task ID: {result.id}")
        return {"message": "Crawling tasks initiated for all selected visas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






