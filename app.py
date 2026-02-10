import streamlit as st
from logic import load_data, find_eligible_pilots, find_eligible_drones

st.set_page_config(page_title="Skylark Ops Agent", layout="wide")

st.title("🚁 Skylark Drones – Operations Coordinator AI")

pilots_df, drones_df, missions_df = load_data()

mission_ids = missions_df["project_id"].tolist()
selected_mission_id = st.selectbox("Select Mission", mission_ids)

mission = missions_df[missions_df["project_id"] == selected_mission_id].iloc[0]

st.subheader("📌 Mission Details")
st.json(mission.to_dict())

st.subheader("👨‍✈️ Eligible Pilots")
eligible_pilots = find_eligible_pilots(mission, pilots_df, missions_df)
st.dataframe(eligible_pilots)

st.subheader("🚁 Eligible Drones")
eligible_drones = find_eligible_drones(mission, drones_df)
st.dataframe(eligible_drones)
