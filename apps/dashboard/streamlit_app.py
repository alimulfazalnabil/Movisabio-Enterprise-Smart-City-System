import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="MoviSabio Command Center", layout="wide")

st.title("🚦 MoviSabio Territorial Intelligence")
st.markdown("### Tenant: City of Campinas | Region: São Paulo")

mode = st.sidebar.radio("Platform Module", [
    "Live Camera (Edge)", 
    "Corridor Coordination",
    "Digital Twin & What-If",
    "Enterprise Command Center",
    "MLOps & Security",
    "Shadow Pilot (Field Validation)",
        "SaaS Tenant Management (Multi-City)",
    "Controlled Field Pilot (LIVE)"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### EDGE AI HEALTH (CAM-001)")
st.sidebar.markdown("Status: **ONLINE**")
st.sidebar.markdown("Camera FPS: **24.0**")
st.sidebar.markdown("Inference Latency: **31.4 ms**")
st.sidebar.markdown("Detection Confidence: **94%**")

if mode == "Enterprise Command Center":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### PLATFORM STATUS")
    st.sidebar.markdown("Tenant: **Campinas-01**")
    st.sidebar.markdown("Data Layer: **PostGIS ONLINE**")
    st.sidebar.markdown("Event Bus: **Kafka ACTIVE**")
    
    st.subheader("Global Territorial Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Intersections", value="24", delta="Active")
    col2.metric(label="Edge Nodes Online", value="22", delta="-2 Offline", delta_color="inverse")
    col3.metric(label="Global Congestion Index", value="0.45", delta="-0.02 (Improving)")
    
    st.markdown("---")
    st.markdown("### Cross-Domain Intelligence")
    colA, colB, colC = st.columns(3)
    colA.info("**Mobility**: 4 Active Green Waves")
    colB.success("**Environment**: AQI 42 (Good)")
    colC.warning("**Incidents**: 1 Minor Accident (Resolved)")

elif mode == "Digital Twin & What-If":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### SIMULATION ENGINE")
    st.sidebar.markdown("Engine: **SUMO Cloud**")
    st.sidebar.markdown("Scenario: **Demand +20%**")
    
    st.subheader("What-If Scenario Analysis")
    st.markdown("Running scenario against Digital Twin: `INT-001`")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Scenario A (Current AI)")
        st.metric("Avg Delay", "31.4 s")
        st.metric("Avg Queue", "11 vehicles")
    with col2:
        st.markdown("#### Scenario B (Demand +20%)")
        st.metric("Avg Delay", "45.2 s", delta="+13.8 s", delta_color="inverse")
        st.metric("Avg Queue", "22 vehicles", delta="+11 vehicles", delta_color="inverse")

elif mode == "MLOps & Security":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### SECURITY STATUS")
    st.sidebar.markdown("Authentication: **OAuth2 ACTIVE**")
    st.sidebar.markdown("WAF: **BLOCKING**")
    st.sidebar.markdown("Audit Log: **ENFORCED**")
    
    st.subheader("Model Registry & MLOps")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Perception (YOLO)")
        st.info("v4.2.1 | **PRODUCTION**")
        st.text("Recall: 0.96 | Drift: Low")
    with col2:
        st.markdown("#### Demand Predictor (LSTM)")
        st.success("v1.8.0 | **PRODUCTION**")
        st.text("MAE: 1.2 | Drift: Stable")
    with col3:
        st.markdown("#### Signal Optimizer (PPO)")
        st.warning("v0.9.4 | **SHADOW MODE**")
        st.text("Reward: +14% | Awaiting Approval")
        
    st.markdown("---")
    st.subheader("Security Audit Log (Live)")
    st.code('''[2026-09-30 18:24:01] [Auth] USER operator-17 Authenticated (MFA)
[2026-09-30 18:24:05] [Controller] REJECTED - Optimizer PPO-0.9.4 attempted phase switch. Reason: SHADOW_MODE_ONLY
[2026-09-30 18:24:12] [Safety] PASSED - Fallback controller maintained green wave.
[2026-09-30 18:24:45] [Edge] API Key rotated for CAM-004
''', language="log")

elif mode == "Shadow Pilot (Field Validation)":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### PILOT STATUS")
    st.sidebar.markdown("Intersection: **INT-001 (Main & 1st)**")
    st.sidebar.markdown("Control Mode: **SHADOW**")
    st.sidebar.markdown("Physical Signal: **UNCHANGED**")
    
    st.subheader("Shadow Mode: Live AI Validation")
    st.warning("MoviSabio is generating live traffic control recommendations. **No commands are being sent to physical hardware.**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Live Recommendation")
        st.info("**ACTION**: EXTEND_GREEN (N/S)")
        st.text("Reason: N_Queue = 12 | S_Queue = 8")
        st.text("Safety Status: PASSED (Min Green Met)")
        st.button("Approve (HIL)", key="hil_approve", help="Send to hardware")
    
    with col2:
        st.markdown("#### Pilot Evidence vs Baseline")
        st.metric("Avg Delay (Shadow vs Baseline)", "38.2 s", delta="-6.8 s (15.1%)", delta_color="inverse")
        st.metric("Throughput (Shadow vs Baseline)", "1350 vph", delta="+150 vph", delta_color="normal")
        st.progress(0.998, text="Safety Pass Rate (99.8%)")

elif mode ==     "SaaS Tenant Management (Multi-City)",
    "Controlled Field Pilot (LIVE)":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ CRITICAL CONTROL")
    st.sidebar.markdown("Intersection: **INT-001**")
    st.sidebar.markdown("Control Mode: **AI + HIL SUPERVISION**")
    st.sidebar.markdown("Fallback Sys: **READY**")
    
    st.error("🚨 LIVE TRAFFIC CONTROL IS ACTIVE 🚨")
    
    st.subheader("Physical Intersection Actuation")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🟢 Current Phase: **N/S Green**")
        st.text("Elapsed Time: 14 seconds")
        st.text("Min Green: MET ✅")
        st.text("Max Green: REMAINING (106s)")
    with col2:
        st.warning("🤖 Pending AI Command")
        st.text("Action: NEXT_PHASE")
        st.text("Confidence: 96%")
        
    st.markdown("---")
    st.markdown("### Operator Controls")
    c1, c2, c3 = st.columns(3)
    c1.button("✅ APPROVE COMMAND", use_container_width=True)
    c2.button("🚫 REJECT COMMAND", use_container_width=True)
    c3.button("🛑 TRIGGER FALLBACK (DISCONNECT AI)", type="primary", use_container_width=True)

elif mode == "Corridor Coordination":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### NETWORK STATUS")
    st.sidebar.markdown("Topology: **4 Intersections**")
    st.sidebar.markdown("Sync: **GREEN WAVE ACTIVE**")
    
    st.subheader("MoviSabio Traffic Operations Center")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🟢 INT-001")
        st.text("Flow: 1400 vph")
        st.text("Queue: 12")
        st.text("Offset: 0s (Master)")
    with col2:
        st.info("🟢 INT-002")
        st.text("Flow: 1350 vph")
        st.text("Queue: 8")
        st.text("Offset: +30s")
    with col3:
        st.warning("🟡 INT-003")
        st.text("Flow: 1520 vph")
        st.text("Queue: 48 (Spillback Risk)")
        st.text("Offset: +71s")
    with col4:
        st.error("🔴 INT-004")
        st.text("Flow: 900 vph")
        st.text("Queue: 5")
        st.text("Offset: +102s")
        
    st.markdown("---")
    st.subheader("Corridor KPIs")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Network Delay", "24.2 s", "-4.1 s")
    kpi2.metric("Corridor Travel Time", "4m 12s", "-45 s")
    kpi3.metric("Throughput", "8,942 vph", "+8.2%")
    kpi4.metric("CO2 Estimate", "2.1 MT", "-0.4 MT")
    
    st.markdown("---")
    st.subheader("Transit & Emergency Priority")
    st.code('''[2026-09-30 18:25:01] [Priority] AMBULANCE DETECTED near INT-002. Approaching INT-003.
[2026-09-30 18:25:02] [Safety] AI requested preemptive Green for INT-003. PASSED.
[2026-09-30 18:25:03] [Control] INT-003 preempted to N/S Green.
[2026-09-30 18:25:40] [Control] Ambulance cleared. Re-syncing green wave offsets.
''', language="log")

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

# --- Prediction & Forecast ---
st.subheader("Traffic Forecast (Next 15 min)")
fc1, fc2, fc3, fc4 = st.columns(4)
fc1.metric("+5 min Vehicles", data["vehicles"] + np.random.randint(5, 15))
fc2.metric("+10 min Vehicles", data["vehicles"] + np.random.randint(15, 30))
fc3.metric("+15 min Vehicles", data["vehicles"] + np.random.randint(25, 45))
fc4.info("Forecast Status: Traffic increase expected. Preparing E/W capacity.")

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
