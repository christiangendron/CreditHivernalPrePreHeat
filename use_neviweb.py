import requests
import logging
import os


def activate_preheat():
    logging.info("=====================================")
    logging.info("Activating the preheat on neviweb...")

    # Open a session
    session = requests.Session()
    resp = session.post(f"https://neviweb.com/api/login",json={"username": os.environ['NEVIWEB_USERNAME'], "password": os.environ['NEVIWEB_PASSWORD'], "interface": "neviweb"}).json()
    if 'error' in resp:
        logging.info(f"Error logging in to neviweb: {resp}")
        return
    data = resp
    session_id = data["session"]
    session.headers["session-id"] = session_id

    # Get devices list
    devices = session.get("https://neviweb.com/api/devices").json()

    for device in devices:
        # We do nothing on a GT130
        if device['family'] == 'GT130':
            logging.info("Skipping: family is GT130")
            continue

        if device['family'] == '339':
            logging.info("Skipping: family is 339")
            continue

        if device['name'] == 'Bedroom':
            logging.info("Skipping: name is Bedroom")
            continue

        # Set the temperature at 26 on each other device
        device_id = device['id']
        setpoint_res = session.put(f"https://neviweb.com/api/device/{device_id}/attribute", json={ "roomSetpoint": 27}).json()

        if 'error' in setpoint_res:
            logging.error(f"❌ Error setting setpoint for device {device_id}: {setpoint_res}")
            continue

        logging.info(setpoint_res)

    # Logout from neviweb to not keep an open session
    _ = session.get(f"https://neviweb.com/api/logout").json()


def activate_shed():
    logging.info("=====================================")
    logging.info("Activating the shed on neviweb...")

    # Open a session
    session = requests.Session()
    resp = session.post(f"https://neviweb.com/api/login",json={"username": os.environ['NEVIWEB_USERNAME'], "password": os.environ['NEVIWEB_PASSWORD'], "interface": "neviweb"}).json()
    if 'error' in resp:
        logging.info(f"Error logging in to neviweb: {resp}")
        return
    data = resp
    session_id = data["session"]
    session.headers["session-id"] = session_id

    # Get devices list
    devices = session.get(f"https://neviweb.com/api/devices").json()

    for device in devices:
        # We do nothing on a GT130
        if device['family'] == 'GT130':
            logging.info("Skipping: family is GT130")
            continue

        if device['family'] == '339':
            logging.info("Skipping: family is 339")
            continue

        # Set the temperature at 10 on each other device
        device_id = device['id']
        setpoint_res = session.put(f"https://neviweb.com/api/device/{device_id}/attribute", json={ "roomSetpoint": 10}).json()

        logging.info(setpoint_res)

    # Logout from neviweb to not keep an open session
    _ = session.get(f"https://neviweb.com/api/logout").json()
