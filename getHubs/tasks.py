import asyncio

from parsingHabr.celery import app
from utils.celery_tasks.req_main_hub import RequestHub


# Create task
@app.task(bind=True)
def request_to_main_hub(self):
    try:
        # Running the parser asynchronously
        request_hub = RequestHub()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(request_hub.run())
    except Exception as exc:
        print("Exception request to main hub: ", exc)
