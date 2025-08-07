# backend/app/routes.py
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import FileResponse, JSONResponse
from .crawler import crawl_website
from .storage import store_job, get_job, update_job
from .utils import validate_urls, process_uploaded_file
from .limiter import limiter

router = APIRouter()

@router.post("/submit-urls")
@limiter.limit("10/minute")
async def submit_urls(
    urls: list[str] = Query(default=[]),
    file: UploadFile = File(None),
    background_tasks: BackgroundTasks
):
    try:
        # Process input
        if file:
            file_urls = await process_uploaded_file(file)
            urls.extend(file_urls)
        
        if not urls:
            raise HTTPException(status_code=400, detail="No valid URLs provided")
        
        # Validate URLs
        valid_urls = validate_urls(urls)
        if not valid_urls:
            raise HTTPException(status_code=400, detail="No valid URLs found")
        
        # Create job
        job_id = str(uuid.uuid4())
        store_job(job_id, {"status": "pending", "urls": valid_urls})
        
        # Start crawling
        background_tasks.add_task(crawl_website, job_id, valid_urls)
        
        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job-status/{job_id}")
def get_job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/export/{job_id}")
def export_results(
    job_id: str,
    format: str = Query(..., regex="^(csv|excel|pdf)$")
):
    job = get_job(job_id)
    if not job or job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not available for export")
    
    # Implementation would create file in /tmp
    file_path = f"/tmp/{job_id}.{format}"
    
    # In a real implementation, we'd generate the file here
    # For demo, return dummy file
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=f"results.{format}"
    )
