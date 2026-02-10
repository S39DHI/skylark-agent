import pandas as pd

def normalize_list_column(df, column):
    df[column] = df[column].fillna("").apply(
        lambda x: [i.strip().lower() for i in x.split(",") if i.strip()]
    )
    return df

def dates_overlap(s1, e1, s2, e2):
    return not (e1 < s2 or e2 < s1)

def load_data():
    pilots = pd.read_csv("pilot_roster.csv")
    drones = pd.read_csv("drone_fleet.csv")
    missions = pd.read_csv("missions.csv")

    missions["start_date"] = pd.to_datetime(missions["start_date"])
    missions["end_date"] = pd.to_datetime(missions["end_date"])

    pilots = normalize_list_column(pilots, "skills")
    pilots = normalize_list_column(pilots, "certifications")
    drones = normalize_list_column(drones, "capabilities")
    missions = normalize_list_column(missions, "required_skills")

    return pilots, drones, missions

def pilot_has_conflict(pilot, mission, missions):
    if pd.isna(pilot["current_assignment"]):
        return False
    m = missions[missions["project_id"] == pilot["current_assignment"]]
    if m.empty:
        return False
    m = m.iloc[0]
    return dates_overlap(
        m["start_date"], m["end_date"],
        mission["start_date"], mission["end_date"]
    )

def find_pilots(mission, pilots, missions):
    out = []
    for _, p in pilots.iterrows():
        if p["status"].lower() != "available":
            continue
        if p["location"].lower() != mission["location"].lower():
            continue
        if not set(mission["required_skills"]).issubset(set(p["skills"])):
            continue
        if pilot_has_conflict(p, mission, missions):
            continue
        out.append(p)
    return pd.DataFrame(out)

def find_drones(mission, drones):
    out = []
    for _, d in drones.iterrows():
        if d["status"].lower() != "available":
            continue
        if d["maintenance_due"].lower() == "yes":
            continue
        if d["location"].lower() != mission["location"].lower():
            continue
        if not set(mission["required_skills"]).issubset(set(d["capabilities"])):
            continue
        out.append(d)
    return pd.DataFrame(out)

def assign_resources(mission_id, pilot_id, drone_id):
    pilots = pd.read_csv("pilot_roster.csv")
    drones = pd.read_csv("drone_fleet.csv")

    pilots.loc[pilots["pilot_id"] == pilot_id, "status"] = "Unavailable"
    pilots.loc[pilots["pilot_id"] == pilot_id, "current_assignment"] = mission_id
    drones.loc[drones["drone_id"] == drone_id, "current_assignment"] = mission_id

    pilots.to_csv("pilot_roster.csv", index=False)
    drones.to_csv("drone_fleet.csv", index=False)
