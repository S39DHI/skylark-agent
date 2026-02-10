import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPE
)

client = gspread.authorize(creds)

sheet = client.open("Skylark Drone Database")
print("Connected to:", sheet.title)
