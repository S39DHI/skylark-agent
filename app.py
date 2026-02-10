import streamlit as st
from logic import load_data, find_pilots, find_drones, assign

st.set_page_config(layout="wide")
st.title("🚁 Skylark Drones – Ops Coordinator AI")

pilots, drones, missions = load_data()

mission_id = st.selectbox("Select Mission", missions["project_id"])
mission = missions[missions["project_id"] == mission_id].iloc[0]

st.subheader("Mission")
st.json(mission.to_dict())

eligible_pilots = find_pilots(mission, pilots, missions)
eligible_drones = find_drones(mission, drones)

st.subheader("Eligible Pilots")
st.dataframe(eligible_pilots)

st.subheader("Eligible Drones")
st.dataframe(eligible_drones)

if eligible_pilots.empty or eligible_drones.empty:
    st.error("⚠️ URGENT REASSIGNMENT REQUIRED")
    st.warning("No immediate pilot or drone available. Consider nearby location or next availability.")
else:
    pilot_id = st.selectbox("Select Pilot", eligible_pilots["pilot_id"])
    drone_id = st.selectbox("Select Drone", eligible_drones["drone_id"])

    if st.button("✅ Assign Resources"):
        assign(mission_id, pilot_id, drone_id)
        st.success("Assignment completed and saved")
