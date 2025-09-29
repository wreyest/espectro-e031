
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# ---- Título ----
st.title("Espectro de Respuesta Sísmica - Norma E.031")

# ---- Parámetros interactivos ----
Z = st.slider("Zona sísmica (Z)", 0.10, 0.50, 0.45, 0.01)
S = st.slider("Factor de importancia (S)", 0.8, 1.5, 1.0, 0.1)
U = st.slider("Factor de uso (U)", 0.8, 1.5, 1.0, 0.1)
Tp = st.slider("Periodo de transición Tp (s)", 0.1, 1.0, 0.4, 0.05)
Tl = st.slider("Periodo largo Tl (s)", 1.0, 5.0, 2.5, 0.1)
g = 1.0   # unidad en g

# ---- Funciones ----
def C(T, Tp, Tl):
    if T < 0:
        return 0
    elif T < 0.2 * Tp:
        return 1 + 7.5 * (T / Tp)
    elif 0.2 * Tp <= T <= Tp:
        return 2.5
    elif Tp < T < Tl:
        return 2.5 * (Tp / T)
    else:
        return 2.5 * (Tp * Tl) / (T ** 2)

def Sa(T, Z, S, U, Tp, Tl):
    return 1.5 * Z * C(T, Tp, Tl) * S * U * g

# ---- Cálculo ----
T_values = np.linspace(0.00, 4.5, 400)
Sa_values = np.array([Sa(T, Z, S, U, Tp, Tl) for T in T_values])

# ---- Gráfico ----
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(T_values, Sa_values, label='Espectro E.031', color='darkblue', linewidth=2)
ax.fill_between(T_values, 0, Sa_values, where=(T_values <= 0.2 * Tp), color='lightblue', alpha=0.3,
                label='Zona periodo corto (T < 0.2 Tp)')
ax.set_title(f"Espectro de Respuesta Sísmica E.031\n(Z={Z}, S={S}, U={U})")
ax.set_xlabel("Periodo (s)")
ax.set_ylabel("Aceleración Espectral Sa (g)")
ax.grid(True)
ax.legend()
ax.set_xlim(0, 4.5)
ax.set_ylim(0, max(Sa_values)*1.1)

st.pyplot(fig)

# ---- Exportar a TXT ----
output = io.StringIO()
output.write("T\tSa\n")
for T, Sa_val in zip(T_values, Sa_values):
    output.write(f"{T:.4f}\t{Sa_val:.4f}\n")

txt_data = output.getvalue()

st.download_button(
    label="📥 Descargar espectro en TXT",
    data=txt_data,
    file_name="espectro_E031.txt",
    mime="text/plain"
)
