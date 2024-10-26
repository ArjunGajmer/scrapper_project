import logging
import time

from app.services.schedular import ScrappingSchedular

if __name__ == "__main__":
    while True:
        scheduled_requests = ScrappingSchedular().run()
        logging.info(f"Scheduled Request total: {scheduled_requests}")
        time.sleep(1)
