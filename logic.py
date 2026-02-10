import pandas as pd

# ------------------------
# Utility functions
# ------------------------

def normalize_list_column(df, column):
    df[column] = df[column].fillna("").apply(
        lambda x: [i.strip().lower() for i in x.split(",") if i.strip()]
    )
    return df


def dates_overlap(start1, end1, start2, end2):
    return not (end1 < start2 or end2 < start1)


# ------------------------
# Load data
# ------------------------

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


# ------------------------
# Pilot logic
# ------------------------

def pilot_is_available(pilot):
    return pilot["status"].lower() == "available"


def pilot_is_qualified(pilot, mission):
    return set(mission["required_skills"]).issubset(set(pilot["skills"]))


def pilot_has_conflict(pilot, mission, missions_df):
    if pd.isna(pilot["current_assignment"]):
        return False

    assigned = missions_df[
        missions_df["project_id"] == pilot["current_assignment"]
    ]

    for _, m in assigned.iterrows():
        if dates_overlap(
            m["start_date"], m["end_date"],
            mission["start_date"], mission["end_date"]
        ):
            return True
    return False


def find_eligible_pilots(mission, pilots_df, missions_df):
    eligible = []

    for _, pilot in pilots_df.iterrows():
        if not pilot_is_available(pilot):
            continue
        if pilot["location"].lower() != mission["location"].lower():
            continue
        if not pilot_is_qualified(pilot, mission):
            continue
        if pilot_has_conflict(pilot, mission, missions_df):
            continue

        eligible.append(pilot)

    return pd.DataFrame(eligible)


# ------------------------
# Drone logic
# ------------------------

def drone_is_available(drone):
    return drone["status"].lower() == "available"


def drone_is_compatible(drone, mission):
    return set(mission["required_skills"]).issubset(set(drone["capabilities"]))


def find_eligible_drones(mission, drones_df):
    eligible = []

    for _, drone in drones_df.iterrows():
        if not drone_is_available(drone):
            continue
        if drone["maintenance_due"].lower() == "yes":
            continue
        if drone["location"].lower() != mission["location"].lower():
            continue
        if not drone_is_compatible(drone, mission):
            continue

        eligible.append(drone)

    return pd.DataFrame(eligible)
