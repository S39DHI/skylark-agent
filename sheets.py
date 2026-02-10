import os
import json
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from environment variable
def get_client():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS environment variable not set")

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)

    return gspread.authorize(creds)


client = get_client()

SHEET_NAME = os.getenv("SHEET_NAME", "Skylark Drone Database")


def load_pilots():
    ws = client.open(SHEET_NAME).worksheet("Pilot_Roster")
    return pd.DataFrame(ws.get_all_records())


def load_drones():
    ws = client.open(SHEET_NAME).worksheet("Drone_Fleet")
    return pd.DataFrame(ws.get_all_records())


def load_missions():
    ws = client.open(SHEET_NAME).worksheet("Missions")
    return pd.DataFrame(ws.get_all_records())


def update_pilot_status(pilot_name, new_status):
    ws = client.open(SHEET_NAME).worksheet("Pilot_Roster")
    records = ws.get_all_records()
    headers = ws.row_values(1)

    status_col = headers.index("status") + 1

    for i, row in enumerate(records, start=2):
        if row["name"].lower() == pilot_name.lower():
            ws.update_cell(i, status_col, new_status)
            return f"{pilot_name} status updated to {new_status}"

    return "Pilot not found"


def update_drone_status(drone_id, new_status):
    ws = client.open(SHEET_NAME).worksheet("Drone_Fleet")
    records = ws.get_all_records()
    headers = ws.row_values(1)

    status_col = headers.index("status") + 1

    for i, row in enumerate(records, start=2):
        if str(row["drone_id"]).lower() == str(drone_id).lower():
            ws.update_cell(i, status_col, new_status)
            return f"Drone {drone_id} status updated to {new_status}"

    return "Drone not found"
