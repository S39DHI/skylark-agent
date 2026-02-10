import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from sheets import (
    load_pilots,
    load_drones,
    load_missions,
    update_pilot_status,
    update_drone_status
)
from conflict import detect_conflicts

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)


# ---------- Gemini Call ----------
def call_gemini(prompt):
    try:
        response = genai.generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=0
        )
        return response.result
    except Exception as e:
        print("Gemini call failed:", e)
        return ""


# ---------- Core Logic ----------
def find_available_pilots():
    pilots = load_pilots()
    results = pilots[pilots["status"] == "Available"]
    if results.empty:
        return "No available pilots."
    return results[["name", "skills", "location"]].to_string(index=False)


def find_available_drones():
    drones = load_drones()
    results = drones[drones["status"] == "Available"]
    if results.empty:
        return "No available drones."
    return results[["drone_id", "capabilities", "location"]].to_string(index=False)


def match_pilot_to_mission(mission_id):
    missions = load_missions()
    mission = missions[missions["project_id"] == mission_id]

    if mission.empty:
        return "Mission not found."

    # Use correct column names
    required_skill = mission.iloc[0]["required_skills"]
    location = mission.iloc[0]["location"]

    pilots = load_pilots()
    candidates = pilots[
        (pilots["status"] == "Available") &
        (pilots["skills"].str.contains(required_skill, case=False, na=False)) &
        (pilots["location"].str.contains(location, case=False, na=False))
    ]

    if candidates.empty:
        return "No suitable pilot found."

    best = candidates.iloc[0]
    return f"Assign {best['name']} to mission {mission_id}."


def urgent_reassignment(mission_id):
    return match_pilot_to_mission(mission_id)


# ---------- Gemini Interpreter ----------
def interpret_with_gemini(user_message: str):
    if not API_KEY:
        return {"action": "unknown"}

    prompt = f"""
Convert this user message into JSON.

Actions:
- available_pilots
- available_drones
- check_conflicts
- assign_mission
- urgent_reassignment
- set_pilot_status
- set_drone_status

Return only JSON.

User message:
{user_message}
"""

    try:
        text = call_gemini(prompt)
        print("GEMINI RAW OUTPUT:", text)

        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            json_text = text[start:end]
            return json.loads(json_text)

    except Exception as e:
        print("Gemini parse error:", e)

    return {"action": "unknown"}


# ---------- Main Handler ----------
def handle_query(message: str):
    # Try Gemini first
    intent = interpret_with_gemini(message)
    action = intent.get("action")

    if action == "available_pilots":
        return find_available_pilots()

    if action == "available_drones":
        return find_available_drones()

    if action == "check_conflicts":
        pilots = load_pilots()
        drones = load_drones()
        missions = load_missions()
        return detect_conflicts(pilots, drones, missions)

    if action == "assign_mission":
        return match_pilot_to_mission(intent.get("mission_id", ""))

    if action == "urgent_reassignment":
        return urgent_reassignment(intent.get("mission_id", ""))

    if action == "set_pilot_status":
        return update_pilot_status(
            intent.get("pilot_name", ""),
            intent.get("status", "")
        )

    if action == "set_drone_status":
        return update_drone_status(
            intent.get("drone_id", ""),
            intent.get("status", "")
        )

    # ---------- Fallback logic (guaranteed to work) ----------
    msg = message.lower()

    if "available" in msg and "pilot" in msg:
        return find_available_pilots()

    if "available" in msg and "drone" in msg:
        return find_available_drones()

    if "conflict" in msg:
        pilots = load_pilots()
        drones = load_drones()
        missions = load_missions()
        return detect_conflicts(pilots, drones, missions)

    if "assign" in msg:
        words = message.split()
        for w in words:
            if w.upper().startswith("PRJ"):
                return match_pilot_to_mission(w.upper())

    if "urgent" in msg:
        words = message.split()
        for w in words:
            if w.upper().startswith("PRJ"):
                return urgent_reassignment(w.upper())

    if "leave" in msg:
        parts = message.split()
        if len(parts) >= 2:
            return update_pilot_status(parts[1], "On Leave")

    if "available" in msg and "set" in msg:
        parts = message.split()
        if len(parts) >= 2:
            return update_pilot_status(parts[1], "Available")

    # Small talk handling
    msg = message.lower()

    if msg in ["hi", "hello", "hey"]:
        return "Hello! I can help manage pilots, drones, and missions."

    if "help" in msg:
        return (
            "You can ask things like:\n"
            "- Who is available?\n"
            "- Put Arjun on leave\n"
            "- Assign someone to PRJ001\n"
            "- Check conflicts"
        )

    return "I didn’t understand. Try asking about pilots, drones, or missions."
