import logging
import requests
from datetime import datetime, timezone, timedelta
from use_events import handle_event

def check_for_event(plagehoraire, preheat_hours):
    logging.info("=====================================")
    logging.info(f"[{plagehoraire}] Checking for an upcoming DR event with Hydro Quebec API...")

    # get the events
    try:
        hydro_base_url = "https://donnees.hydroquebec.com/"
        sub_url = f"/api/explore/v2.1/catalog/datasets/evenements-pointe/records?limit=100&refine=offre%3ACPC-D&refine=plagehoraire%3A{plagehoraire}&refine=datedebut%3A%222025%22"
        hydro_api_url = hydro_base_url + sub_url
        events = requests.get(hydro_api_url).json()
        events = events['results']
    except Exception as e:
        logging.error(f"[{plagehoraire}] Error fetching events from Hydro Quebec API: {e}")
        return

    if len(events) == 0:
        logging.info(f"[{plagehoraire}] No upcoming events found...")
        return
    else:
        logging.info(f"[{plagehoraire}] Found {len(events)} upcoming events")

    # Check if there's an event in the next preheat_hours hours
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=preheat_hours)
    logging.info(f"[{plagehoraire}] Checking for events between [{now.isoformat()}] and [{window_end.isoformat()}] -  {preheat_hours} hours window")

    for event in events:
        event_start_str = event['datedebut']

        if event_start_str.endswith('Z'):
            event_start_str = event_start_str[:-1] + '+00:00'

        event_start = datetime.fromisoformat(event_start_str)

        if now <= event_start <= window_end:
            logging.info(f"[{plagehoraire}] ✅ Found an [{plagehoraire}] event starting at {event_start_str} within the next {preheat_hours} hours!")
            handle_event(event)
            return

    logging.info(f"[{plagehoraire}] ❌ No event within the next {preheat_hours} hours...")