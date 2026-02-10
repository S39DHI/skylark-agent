import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("Skylark Drone Database")

pilot_sheet = sheet.worksheet("Pilot_Roster")
drone_sheet = sheet.worksheet("Drone_Fleet")
mission_sheet = sheet.worksheet("Missions")


def get_pilots():
    return pilot_sheet.get_all_records()


def get_drones():
    return drone_sheet.get_all_records()


def get_missions():
    return mission_sheet.get_all_records()


def update_pilot_status(pilot_name, new_status):
    data = pilot_sheet.get_all_records()

    for i, row in enumerate(data, start=2):
        if row["name"].lower() == pilot_name.lower():
            status_col = list(row.keys()).index("status") + 1
            pilot_sheet.update_cell(i, status_col, new_status)
            return f"{pilot_name} status updated to {new_status}"

    return "Pilot not found"


def assign_pilot_to_project(pilot_name, project_id):
    data = pilot_sheet.get_all_records()

    for i, row in enumerate(data, start=2):
        if row["name"].lower() == pilot_name.lower():
            assignment_col = list(row.keys()).index("current_assignment") + 1
            status_col = list(row.keys()).index("status") + 1

            pilot_sheet.update_cell(i, assignment_col, project_id)
            pilot_sheet.update_cell(i, status_col, "Assigned")

            return f"{pilot_name} assigned to {project_id}"

    return "Pilot not found"
