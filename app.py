import streamlit as st
from logic import (
    load_data,
    find_pilots,
    find_drones,
    assign_resources
)

st.set_page_config(layout="wide")
st.title("🚁 Skylark Drones – Operations Coordinator AI Agent")

# Load data
pilots, drones, missions = load_data()

# Conversational Agent Input
st.subheader("🤖 Agent Command")
command = st.text_input(
    "Ask the agent (examples: assign resources, check conflicts, urgent reassignment)"
)

# Mission Selection
st.subheader("Select Mission")
mission_id = st.selectbox("Mission", missions["project_id"])
mission = missions[missions["project_id"] == mission_id].iloc[0]

st.subheader("📌 Mission Details")
st.json(mission.to_dict())

# Agent Reasoning Feedback
if command:
    cmd = command.lower()
    if "assign" in cmd:
        st.info("Agent intent: Resource assignment")
    if "conflict" in cmd:
        st.info("Agent intent: Conflict analysis")
    if "urgent" in cmd or "reassign" in cmd:
        st.warning("Agent intent: Urgent reassignment protocol triggered")

# Find resources
eligible_pilots = find_pilots(mission, pilots, missions)
eligible_drones = find_drones(mission, drones)

st.subheader("👨‍✈️ Eligible Pilots")
st.dataframe(eligible_pilots)

st.subheader("🚁 Eligible Drones")
st.dataframe(eligible_drones)

# Decision + Action
if eligible_pilots.empty or eligible_drones.empty:
    st.error("⚠️ URGENT REASSIGNMENT REQUIRED")
    st.warning(
        "No immediate pilot or drone available. "
        "Consider nearby location or next availability."
    )
else:
    pilot_id = st.selectbox("Select Pilot", eligible_pilots["pilot_id"])
    drone_id = st.selectbox("Select Drone", eligible_drones["drone_id"])

    if st.button("✅ Assign Resources"):
        assign_resources(mission_id, pilot_id, drone_id)
        st.success("Assignment completed and saved")
