import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("1D Heat Transfer Simulation")

length = st.sidebar.number_input("Length (m)", value=1.0, min_value=0.1, step=0.1)
nx = st.sidebar.slider("Number of Spatial Points", min_value=10, max_value=200)
# Material selection and thermal diffusivity calculation
materials = {
    "Aluminum": {"k": 205, "rho": 2700, "cp": 900},
    "Copper": {"k": 385, "rho": 8960, "cp": 385},
    "Steel": {"k": 45, "rho": 7850, "cp": 500},
    "Custom": None
}

material = st.sidebar.selectbox("Material", list(materials.keys()))
if material != "Custom":
    k = materials[material]["k"]
    rho = materials[material]["rho"]
    cp = materials[material]["cp"]
    alpha = k / (rho * cp)
    st.sidebar.write(f"Computed Thermal Diffusivity α = {alpha:.2e} m²/s")
else:
    k = st.sidebar.number_input("Thermal Conductivity k (W/m·K)", value=1.0, min_value=0.0, format="%.2f")
    rho = st.sidebar.number_input("Density ρ (kg/m³)", value=1000.0, min_value=0.0, format="%.1f")
    cp = st.sidebar.number_input("Specific Heat cp (J/kg·K)", value=1000.0, min_value=0.0, format="%.1f")
    alpha = k / (rho * cp)
dx = length / (nx - 1)
dt = st.sidebar.number_input("Time Step (s)", value=0.01)
total_time = st.sidebar.number_input("Total Simulation Time (s)", value=5.0)
nt = int(total_time / dt)
left_temp = st.sidebar.number_input("Left Boundary Temperature (C)", value=100.0)
init_temp = st.sidebar.number_input("Initial Temperature (C)", value=25.0)

if st.sidebar.button("Run Simulation"):
    
    stability = alpha * dt / dx**2

    
    T = np.ones(nx) * init_temp
    T[0] = left_temp

    
    T_record = [T.copy()]
    for _ in range(nt):
        Tn = T.copy()
        for i in range(1, nx-1):
            T[i] = Tn[i] + stability * (Tn[i+1] - 2*Tn[i] + Tn[i-1])
        T[0] = left_temp
        T[-1] = T[-2]  # Adiabatic right boundary: zero temperature gradient
        T_record.append(T.copy())

   
    T_array = np.array(T_record)
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, length, nx), T_array[-1])
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title(f"Temperature at t = {total_time:.2f} s")
    st.pyplot(fig)