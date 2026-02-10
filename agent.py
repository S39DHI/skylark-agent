from sheets import (
    load_pilots,
    load_drones,
    load_missions,
    update_pilot_status,
    update_drone_status
)
from conflict import detect_conflicts


def find_available_pilots(skill=None, location=None):
    pilots = load_pilots()
    results = pilots[pilots["status"] == "Available"]

    if skill:
        results = results[
            results["skills"].str.contains(skill, case=False, na=False)
        ]

    if location:
        results = results[
            results["location"].str.contains(location, case=False, na=False)
        ]

    return results


def find_available_drones(capability=None, location=None):
    drones = load_drones()
    results = drones[drones["status"] == "Available"]

    if capability:
        results = results[
            results["capabilities"].str.contains(capability, case=False, na=False)
        ]

    if location:
        results = results[
            results["location"].str.contains(location, case=False, na=False)
        ]

    return results


def match_pilot_to_mission(mission_id):
    missions = load_missions()
    mission = missions[missions["project_id"] == mission_id]

    if mission.empty:
        return "Mission not found."

    required_skill = mission.iloc[0]["required_skills"]
    location = mission.iloc[0]["locations"]

    candidates = find_available_pilots(required_skill, location)

    if candidates.empty:
        return "No suitable pilot found."

    best = candidates.iloc[0]
    return f"Assign {best['name']} to mission {mission_id}."


def urgent_reassignment(mission_id):
    missions = load_missions()
    mission = missions[missions["project_id"] == mission_id]

    if mission.empty:
        return "Mission not found."

    required_skill = mission.iloc[0]["required_skills"]
    location = mission.iloc[0]["locations"]

    candidates = find_available_pilots(required_skill, location)

    if candidates.empty:
        return "No urgent replacement available."

    best = candidates.iloc[0]
    return f"Urgent reassignment: {best['name']} is best replacement."


def handle_query(message: str):
    message = message.lower()

    # Pilot queries
    if "available" in message and "pilot" in message:
        results = find_available_pilots()
        if results.empty:
            return "No available pilots."
        return results[["name", "skills", "location"]].to_string(index=False)

    # Drone queries
    if "available" in message and "drone" in message:
        results = find_available_drones()
        if results.empty:
            return "No available drones."
        return results[["drone_id", "capabilities", "location"]].to_string(index=False)

    # Conflict detection
    if "conflict" in message:
        pilots = load_pilots()
        drones = load_drones()
        missions = load_missions()
        return detect_conflicts(pilots, drones, missions)

    # Assign mission
    if "assign" in message:
        mission_id = message.split()[-1].upper()
        return match_pilot_to_mission(mission_id)

    # Urgent reassignment
    if "urgent" in message:
        mission_id = message.split()[-1].upper()
        return urgent_reassignment(mission_id)

    # Update pilot status
    if "set" in message and "status" in message and "drone" not in message:
        parts = message.split()
        pilot_name = parts[1]
        new_status = " ".join(parts[3:])
        return update_pilot_status(pilot_name, new_status)

    # Update drone status
    if "set" in message and "drone" in message:
        parts = message.split()
        drone_id = parts[2]
        new_status = " ".join(parts[4:])
        return update_drone_status(drone_id, new_status)

    return (
        "Try:\n"
        "- available pilots\n"
        "- available drones\n"
        "- check conflicts\n"
        "- assign M1\n"
        "- urgent M1\n"
        "- set Arjun status Available\n"
        "- set drone D1 status Maintenance"
    )
