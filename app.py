import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="MoviSabio Command Center", layout="wide")

st.title("🚦 MoviSabio Traffic Command Center")
st.markdown("### Intersection: INT-001 (Main St & 1st Ave)")

# --- Mock Live Data ---
if 'time' not in st.session_state:
    st.session_state.time = 18

def get_live_data():
    return {
        "vehicles": np.random.randint(100, 150),
        "avg_speed": round(np.random.uniform(25.0, 35.0), 1),
        "queue": np.random.randint(30, 50),
        "congestion": round(np.random.uniform(0.5, 0.8), 2)
    }

data = get_live_data()

# --- Top Dashboard KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Vehicles", data["vehicles"])
col2.metric("Avg Speed (km/h)", data["avg_speed"])
col3.metric("Total Queue", data["queue"])
col4.metric("Congestion Index", data["congestion"])

st.divider()

# --- Signal & Lane Stats ---
col_sig, col_lanes = st.columns(2)

with col_sig:
    st.subheader("Current Signal State")
    st.markdown("### N/S Phase: 🟢 GREEN")
    st.markdown("### E/W Phase: 🔴 RED")
    
    # Progress bar for remaining time
    st.markdown(f"**Remaining: {st.session_state.time} sec**")
    st.progress(st.session_state.time / 30.0)
    
    if st.button("Refresh Stream"):
        st.session_state.time -= 2
        if st.session_state.time <= 0:
            st.session_state.time = 30
        st.rerun()

with col_lanes:
    st.subheader("Lane Statistics")
    lane_data = pd.DataFrame({
        "Lane": ["N1", "N2", "E1", "E2"],
        "Vehicles": [12, 19, 27, 22],
        "Speed (km/h)": [32, 25, 18, 20],
        "Queue": [3, 8, 14, 11]
    })
    st.dataframe(lane_data, use_container_width=True, hide_index=True)

st.divider()

# --- Audit Log & Telemetry ---
st.subheader("Audit & Command Trail")
audit_df = pd.DataFrame([
    {"time": "21:04:12", "cmd": "CMD-091A", "phase": "NS_GREEN", "safety": "PASSED", "status": "ACKNOWLEDGED"},
    {"time": "21:02:45", "cmd": "CMD-0919", "phase": "EW_GREEN", "safety": "PASSED", "status": "ACKNOWLEDGED"},
    {"time": "21:00:10", "cmd": "CMD-0918", "phase": "NS_GREEN", "safety": "PASSED", "status": "ACKNOWLEDGED"},
])
st.table(audit_df)

st.sidebar.header("System Health")
st.sidebar.success("YOLO Perception: ONLINE")
st.sidebar.success("Traffic State Engine: ONLINE")
st.sidebar.success("Safety Gatekeeper: ONLINE")
st.sidebar.success("SUMO Digital Twin: ONLINE")
