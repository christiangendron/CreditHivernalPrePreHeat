import os
import time
import logging
from use_hydro import check_for_event


def main():
    check_for_event('AM', 6)
    check_for_event('PM', 4)
    logging.info("=====================================")
    logging.info(f"Sleeping for 5 minutes...")
    time.sleep(5 * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s",datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("=====================================")
    logging.info("Starting the script that will automatically activate preheat before a dr event...")
    logging.info(f"Will use {os.environ['NEVIWEB_USERNAME']} on neviweb")

    while True:
        try:
            main()
        except Exception as e:
            last_event_start = None
            logging.error(f"Error in main loop: {e}")
            time.sleep(60)