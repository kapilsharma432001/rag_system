import time
from app.celery_app import celery_app


@celery_app.task
def simulate_ingestion(filename: str):
    print(f"Started processing: {filename}")

    # simulate a time consuming operation
    time.sleep(5)

    print(f"Finished proessing: {filename}")

    return {
        "filename": filename,
        "message": "Processing completed",
    }