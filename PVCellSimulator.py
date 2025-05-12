## PV Cell Simulator App

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import pdfkit
import os
from datetime import datetime

# --------------------------------------------------- FIXED CONSTANTS --------------------------------------------------

k = 1.3805e-23         # Boltzmann constant [J/K]
q = 1.6e-19            # Electron charge [C]

# --------------------------------------------------------- UI ---------------------------------------------------------

st.set_page_config(page_title="PV Cell Simulator", layout="wide")
st.title("🔆 PV Cell Simulator")
st.markdown("Simulate I-V and P-V curves for custom photovoltaic cell parameters.")

# --------------------------------------------------- Sidebar Inputs ---------------------------------------------------

st.sidebar.header("📦 Module Parameters")
Isc_ref = st.sidebar.number_input("Short-circuit current (Isc) [A]", value=7.98)
Voc_ref = st.sidebar.number_input("Open-circuit voltage (Voc) [V]", value=21.9)
Rs = st.sidebar.number_input("Series resistance (Rs) [Ω]", value=0.0001, format="%.4f")
Rsh = st.sidebar.number_input("Shunt resistance (Rsh) [Ω]", value=1000.0)
Ns = st.sidebar.number_input("Number of series cells (Ns)", value=36)

st.sidebar.header("🧪 Model Constants")
n = st.sidebar.number_input("Diode ideality factor (n)", value=1.2)
G_ref = st.sidebar.number_input("Reference irradiance (G_ref) [W/m²]", value=1000)
alpha_Isc = st.sidebar.number_input("Temp. coefficient of Isc (α) [1/°C]", value=0.001904, format="%.6f")

# ----------------------------------------------------- Main Inputs ---------------------------------------------------

G = st.slider("☀️ Irradiance [W/m²]", 0, 1500, 1000, step=50)
temperatures = st.multiselect(
    "🌡️ Temperatures (°C)",
    options=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    default=[0, 20, 40, 60, 80, 100]
)

# -------------------------------------------------- MODEL FUNCTIONS --------------------------------------------------

def photo_current(G, T):
    return Isc_ref * (G / G_ref) * (1 + alpha_Isc * (T - 25))

def reverse_saturation_current(T_K):
    return Isc_ref / (np.exp(q * Voc_ref / (n * Ns * k * T_K)) - 1)

def pv_current(V, Iph, I0, T_K):
    Vt = n * Ns * k * T_K / q
    return Iph - I0 * (np.exp((V + Rs) / Vt) - 1) - (V + Rs) / Rsh

# ----------------------------------------------------- SIMULATION -----------------------------------------------------

V = np.linspace(0, Voc_ref, 100)
fig = make_subplots(rows=1, cols=2, subplot_titles=("I-V Curve", "P-V Curve"))
plot_data = []

for T in temperatures:
    T_K = T + 273
    Iph = photo_current(G, T)
    I0 = reverse_saturation_current(T_K)
    I = pv_current(V, Iph, I0, T_K)
    I = np.clip(I, 0, None)
    P = V * I
    fig.add_trace(go.Scatter(x=V, y=I, mode='lines', name=f'{T}°C – IV'), row=1, col=1)
    fig.add_trace(go.Scatter(x=V, y=P, mode='lines', name=f'{T}°C – PV'), row=1, col=2)
    plot_data.append((T, V, I, P))

fig.update_layout(
    height=500,
    title="Simulation Results",
    xaxis_title="Voltage (V)",
    yaxis_title="Current (A)",
    xaxis2_title="Voltage (V)",
    yaxis2_title="Power (W)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("📘 Developed by **Vitor D. Marchiori** — using Python, Streamlit and Plotly")
st.markdown("[GitHub](https://github.com/vitordmarchiori)")

# --------------------------------------------------------------------------------------------------------------------
# HOW TO RUN THIS APP:
#
# 1. Open a terminal or command prompt.
# 2. Navigate to the folder where this file is located using:
#    cd "path\to\your\folder"
#    (For example: cd "C:\Users\YourUsername\Documents\PVCellSimulator")
#
# 3. Run the app with Streamlit:
#    streamlit run PVCellSimulator.py
#
# Alternatively, provide the full path directly:
#    streamlit run "C:\full\path\to\PVCellSimulator.py"
#
# --------------------------------------------------------------------------------------------------------------------

