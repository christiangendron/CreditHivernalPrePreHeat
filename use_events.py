import requests
import logging
from datetime import datetime, timezone, timedelta
from use_neviweb import activate_preheat, activate_shed

last_event_start = None


def handle_event(event):
    global last_event_start

    logging.info("=====================================")
    logging.info("Handling the upcoming DR event...")

    # Normalize timestamp
    event_start_str = event['datedebut']
    if event_start_str.endswith('Z'):
        event_start_str = event_start_str[:-1] + '+00:00'
    event_start = datetime.fromisoformat(event_start_str)

    now = datetime.now(timezone.utc)
    diff = event_start - now
    minutes_to_event = diff.total_seconds() / 60

    logging.info(f"Event starts in {minutes_to_event:.2f} minutes")

    # Decide which action to take
    if minutes_to_event <= 16:
        logging.info("🧊 Event starts in ≤ 16 minutes → activating SHED")
        activate_shed()
    else:
        if last_event_start is not None and event_start == last_event_start:
            logging.info(f"⚠️ Event starting at {event_start} has already been handled.")
            return

        logging.info("🔥 Event is farther than 16 minutes → activating PREHEAT")
        activate_preheat()

    # Mark as processed
    last_event_start = event_start