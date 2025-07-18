import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(layout="centered")
st.title("📊 Polarization Intensity Histogram")

# Initialize default angles in session state
if "polarizer_angles" not in st.session_state:
    st.session_state.polarizer_angles = [0, 45, 90]

# Light color selection
color_choice = st.selectbox("Choose Light Color", ["Red", "Green", "Blue"])
color_map = {"Red": "crimson", "Green": "seagreen", "Blue": "royalblue"}

# Add/Remove Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Polarizer"):
        st.session_state.polarizer_angles.append(0)
with col2:
    if st.button("➖ Remove Last Polarizer") and len(st.session_state.polarizer_angles) > 2:
        st.session_state.polarizer_angles.pop()

# Manual angle inputs
angles = []
cols = st.columns(len(st.session_state.polarizer_angles))
for i in range(len(st.session_state.polarizer_angles)):
    with cols[i]:
        angle = st.number_input(f"Angle {i+1} (°)", 0, 180, value=st.session_state.polarizer_angles[i], key=f"angle_{i}")
        angles.append(angle)
st.session_state.polarizer_angles = angles

# Intensity calculation
def polarization(theta_deg):
    rad = np.deg2rad(theta_deg)
    return np.array([np.cos(rad), np.sin(rad)])

E = polarization(angles[0])
intensities = [np.linalg.norm(E)**2]
for theta in angles[1:]:
    P = polarization(theta)
    E = np.dot(P, E) * P
    intensities.append(np.linalg.norm(E)**2)

# Plot: Histogram with intensity labels
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar([f"{a}°" for a in angles], intensities, color=color_map[color_choice], edgecolor='black')
ax.set_ylabel("Relative Intensity")
ax.set_title("Intensity After Each Polarizer")
ax.set_ylim([0, 1])

# Add text labels on bars
for bar, intensity in zip(bars, intensities):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height / 2,
            f"{intensity:.2f}", ha='center', va='center', color='white', fontweight='bold')

st.pyplot(fig)

# Download button
buf = BytesIO()
fig.savefig(buf, format="png")
st.download_button("💾 Download Histogram as PNG", buf.getvalue(), file_name="intensity_histogram.png", mime="image/png")
