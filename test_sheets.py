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

data = pilot_sheet.get_all_records()

print("Pilots:")
for row in data:
    print(row)
