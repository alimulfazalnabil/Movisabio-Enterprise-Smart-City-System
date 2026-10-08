import os
import requests
import streamlit as st

st.set_page_config(page_title="MoviSabio AITCS Command Center", layout="wide")

API_URL = os.getenv("AITCS_API_URL", "http://localhost:8000").rstrip("/")

st.title("MoviSabio AITCS Command Center")
st.caption("Investor demonstration surface — simulation/replay only. No physical controller access.")

try:
    health = requests.get(f"{API_URL}/health", timeout=3).json()
    ready_response = requests.get(f"{API_URL}/health/ready", timeout=3)
    ready = ready_response.json()
except Exception as exc:
    health = {"status": "unreachable"}
    ready = {"status": "not_ready", "checks": {"api": str(exc)}}

c1, c2, c3, c4 = st.columns(4)
c1.metric("API", health.get("status", "unknown").upper())
c2.metric("Controller Mode", health.get("controller_mode", "unknown"))
c3.metric("Database", ready.get("checks", {}).get("database", "unknown").upper())
c4.metric("Redis", ready.get("checks", {}).get("redis", "unknown").upper())

st.divider()

st.subheader("Safety Boundary")
st.code(
    "Candidate Plan → Safety Validator → Approved Plan → Simulation/Shadow Adapter",
    language="text",
)
st.info("Physical actuation is intentionally disabled in the investor/demo deployment.")

st.subheader("AITCS Release Status")
status = [
    ("Perception contract", "In engineering hardening"),
    ("Traffic state estimation", "Operational deterministic engine"),
    ("Prediction", "Persistence baseline; ML requires a versioned checkpoint"),
    ("Signal optimization", "Deterministic candidate generation"),
    ("Safety validation", "Mandatory rule-based gate"),
    ("SUMO", "TraCI adapter implemented; scenario validation required"),
    ("Physical controller", "DISABLED"),
]
for component, state in status:
    st.write(f"**{component}:** {state}")

st.divider()
st.subheader("Next Investor Demo")
st.write(
    "Run a recorded traffic scenario through perception/state estimation, "
    "generate a candidate signal plan, validate it through the safety boundary, "
    "and compare the result with a fixed-time baseline in SUMO."
)
