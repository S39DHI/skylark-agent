def detect_conflicts(pilots, drones, missions):
    issues = []

    # Pilot on leave but assigned
    for _, p in pilots.iterrows():
        assignment = str(p.get("current_assignment", "")).strip()
        if p["status"] == "On Leave" and assignment:
            issues.append(
                f"Pilot {p['name']} is on leave but assigned."
            )

    # Drone in maintenance but assigned
    for _, d in drones.iterrows():
        assignment = str(d.get("current_assignment", "")).strip()
        if d["status"] == "Maintenance" and assignment:
            issues.append(
                f"Drone {d['drone_id']} is in maintenance but assigned."
            )

    # Skill mismatch
    for _, m in missions.iterrows():
        required_skill = str(m.get("required_skills", "")).lower()
        assigned_pilot = str(m.get("assigned_pilot", "")).lower()

        if assigned_pilot:
            match = pilots[pilots["name"].str.lower() == assigned_pilot]
            if not match.empty:
                pilot_skills = str(match.iloc[0]["skills"]).lower()
                if required_skill not in pilot_skills:
                    issues.append(
                        f"Skill mismatch: {assigned_pilot} lacks {required_skill} for mission {m['project_id']}."
                    )

    if not issues:
        return "No conflicts detected."

    return "\n".join(issues)
