import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

st.set_page_config(page_title="Prensa hidráulica (Pascal + Trabajo)", layout="wide")

st.title("Simulación': Prensa hidráulica (Principio de Pascal + Conservación de volumen)")

st.markdown(
    """
Modelo ideal:
- Presión:  **F1/A1 = F2/A2**
- Volumen:  **A1·Δx1 = A2·Δx2**
- Trabajo:  **W1 = F1·Δx1**, **W2 = F2·Δx2**  → idealmente **W1 ≈ W2**
"""
)

# ---------- Sidebar: parámetros ----------
st.sidebar.header("Parámetros (editables)")

unit_area = st.sidebar.selectbox("Unidades de área", ["m²", "cm²"], index=1)
area_scale = 1.0 if unit_area == "m²" else 1e-4  # 1 cm² = 1e-4 m²

A1_user = st.sidebar.slider("A1 (área pistón pequeño)", 1.0, 50.0, 5.0, 0.5)
A2_user = st.sidebar.slider("A2 (área pistón grande)", 1.0, 200.0, 50.0, 1.0)

A1 = A1_user * area_scale
A2 = A2_user * area_scale

F1 = st.sidebar.slider("F1 (fuerza aplicada) [N]", 10.0, 2000.0, 200.0, 10.0)

unit_x = st.sidebar.selectbox("Unidades de desplazamiento", ["m", "cm"], index=1)
x_scale = 1.0 if unit_x == "m" else 1e-2  # 1 cm = 1e-2 m

dx1_user = st.sidebar.slider("Δx1 (desplazamiento pistón pequeño)", 0.0, 50.0, 10.0, 0.5)
dx1 = dx1_user * x_scale

# Opción para “animar”
animate = st.sidebar.checkbox("Animar movimiento", value=False)
fps = st.sidebar.slider("FPS (solo si animas)", 5, 30, 15, 1)
duration = st.sidebar.slider("Duración (s, solo si animas)", 1.0, 6.0, 3.0, 0.5)

graph_type = st.sidebar.selectbox(
    "Gráfica",
    [
        "F2 vs (A2/A1)",
        "W2 vs W1",
        "(Δx1/Δx2) vs (A2/A1)"
    ],
    index=0
)

# ---------- Cálculos ----------
# Evitar división por cero (aunque sliders no lo permiten)
ratio_A = A2 / A1
F2 = F1 * ratio_A
dx2 = dx1 * (A1 / A2) if A2 != 0 else 0.0

W1 = F1 * dx1
W2 = F2 * dx2

err = abs(W1 - W2) / (abs(W1) + 1e-12) * 100.0

# ---------- Layout ----------
col1, col2 = st.columns([1.1, 1.0])

# ---------- Visual de la prensa ----------
def draw_press(dx1_m, dx2_m, F1_N, F2_N, A1_m2, A2_m2):
    """
    Dibujo 2D simple: dos cilindros con pistones conectados por fluido.
    La posición de cada pistón depende de dx1 y dx2.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Escalas visuales (no “realistas”, solo para ver bien)
    # Convertimos desplazamientos a unidades de dibujo
    # (si dx es pequeño, igual se ve)
    k = 8.0  # amplificación visual del movimiento
    y0_small = 0.6
    y0_large = 0.6

    # Base del contenedor
    ax.add_patch(Rectangle((0.2, 0.1), 0.6, 0.2, fill=False, linewidth=2))
    ax.add_patch(Rectangle((2.2, 0.1), 0.9, 0.2, fill=False, linewidth=2))

    # Cilindros (paredes)
    ax.add_patch(Rectangle((0.25, 0.3), 0.5, 1.4, fill=False, linewidth=2))
    ax.add_patch(Rectangle((2.25, 0.3), 0.8, 1.4, fill=False, linewidth=2))

    # Conexión (tubo)
    ax.add_patch(Rectangle((0.8, 0.45), 1.4, 0.15, fill=False, linewidth=2))
    ax.add_patch(Rectangle((0.82, 0.47), 1.36, 0.11, alpha=0.15))

    # Pistones (posición variable)
    # El pequeño baja con dx1, el grande sube con dx2 (según convención)
    y_piston_small = 1.35 - k * dx1_m
    y_piston_large = 1.35 + k * dx2_m

    # Nivel “fluido” (solo decoración)
    ax.add_patch(Rectangle((0.27, 0.32), 0.46, y_piston_small - 0.32, alpha=0.15))
    ax.add_patch(Rectangle((2.27, 0.32), 0.76, y_piston_large - 0.32, alpha=0.15))

    # Limitar para no salirse del dibujo
    y_piston_small = np.clip(y_piston_small, 0.45, 1.55)
    y_piston_large = np.clip(y_piston_large, 0.45, 1.55)

    ax.add_patch(Rectangle((0.27, y_piston_small), 0.46, 0.08, linewidth=2, fill=True, alpha=0.4))
    ax.add_patch(Rectangle((2.27, y_piston_large), 0.76, 0.08, linewidth=2, fill=True, alpha=0.4))

    # Flechas de fuerza (tamaño relativo)
    # Escalamos para visual
    fscale = 0.0006
    f1_len = np.clip(F1_N * fscale, 0.1, 0.8)
    f2_len = np.clip(F2_N * fscale, 0.1, 0.8)

    # F1 hacia abajo sobre pistón pequeño
    ax.add_patch(FancyArrow(0.5, y_piston_small + 0.45, 0, -f1_len, width=0.03, length_includes_head=True))
    ax.text(0.12, 1.88, f"F1 = {F1_N:.1f} N", fontsize=11)

    # F2 hacia arriba sobre pistón grande (reacción)
    ax.add_patch(FancyArrow(2.65, y_piston_large - 0.25, 0, f2_len, width=0.03, length_includes_head=True))
    ax.text(1.90, 1.88, f"F2 = {F2_N:.1f} N", fontsize=11)

    # Etiquetas áreas
    ax.text(0.12, 1.78, f"A1 = {A1_user:.2f} {unit_area}", fontsize=10)
    ax.text(1.90, 1.78, f"A2 = {A2_user:.2f} {unit_area}", fontsize=10)

    # Etiquetas desplazamientos
    ax.text(0.12, 0.02, f"Δx1 = {dx1_user:.2f} {unit_x}", fontsize=10)
    ax.text(1.90, 0.02, f"Δx2 = {(dx2_m/x_scale):.2f} {unit_x}", fontsize=10)

    ax.set_xlim(0, 3.4)
    ax.set_ylim(0, 2.0)
    ax.axis("off")
    ax.set_title("Visualización (pistones + transmisión de presión)", fontsize=12)
    return fig

with col1:
    st.subheader("Animación / Funcionamiento visual")

    if not animate:
        fig = draw_press(dx1, dx2, F1, F2, A1, A2)
        st.pyplot(fig)
    else:
        # Animación simple: recorremos dx1 desde 0 hasta el valor actual
        frames = int(max(2, fps * duration))
        placeholder = st.empty()
        for t in np.linspace(0, dx1, frames):
            t_dx2 = t * (A1 / A2)
            fig = draw_press(t, t_dx2, F1, F1*(A2/A1), A1, A2)
            placeholder.pyplot(fig)
        st.caption("Tip: si se ve lento, baja FPS o duración.")

# ---------- Resultados numéricos ----------
with col2:
    st.subheader("Resultados y validaciones")

    c1, c2 = st.columns(2)
    c1.metric("Relación de áreas A2/A1", f"{ratio_A:.3f}")
    c2.metric("F2 (N)", f"{F2:.2f}")

    c3, c4 = st.columns(2)
    c3.metric("Δx1", f"{dx1:.4f} m")
    c4.metric("Δx2", f"{dx2:.4f} m")

    c5, c6 = st.columns(2)
    c5.metric("W1 = F1·Δx1 (J)", f"{W1:.4f}")
    c6.metric("W2 = F2·Δx2 (J)", f"{W2:.4f}")

    if err < 0.5:
        st.success(f"Validación energía: W1 ≈ W2 ✅ (error ≈ {err:.3f}%)")
    else:
        st.warning(f"Validación energía: diferencia notable (error ≈ {err:.3f}%). Revisa parámetros/unidades.")

    st.markdown("**Caso límite:** cuando A2 = A1 → F2 = F1 y Δx2 = Δx1")
    if abs(A2 - A1) / A1 < 1e-9:
        st.info("Estás prácticamente en A2 = A1.")

# ---------- Gráfica ----------
st.subheader("Gráfica (se actualiza con los parámetros)")

fig2, ax2 = plt.subplots(figsize=(9, 4.2))

if graph_type == "F2 vs (A2/A1)":
    # Barrido de razón de áreas manteniendo A1 fijo: A2_var = r*A1
    r = np.linspace(0.5, 10.0, 200)
    F2_curve = F1 * r
    ax2.plot(r, F2_curve)
    ax2.scatter([ratio_A], [F2])
    ax2.set_xlabel("A2/A1")
    ax2.set_ylabel("F2 (N)")
    ax2.set_title("F2 vs relación de áreas (A2/A1)")

elif graph_type == "W2 vs W1":
    # Barrido de dx1 para ver conservación: W2 debería seguir a W1
    dx1_line = np.linspace(0, max(dx1, 0.2), 200)
    dx2_line = dx1_line * (A1 / A2)
    W1_line = F1 * dx1_line
    W2_line = (F1 * (A2 / A1)) * dx2_line
    ax2.plot(W1_line, W2_line)
    ax2.scatter([W1], [W2])
    ax2.set_xlabel("W1 (J)")
    ax2.set_ylabel("W2 (J)")
    ax2.set_title("Trabajo de salida vs trabajo de entrada (ideal: y = x)")

else:  # "(Δx1/Δx2) vs (A2/A1)"
    r = np.linspace(0.5, 10.0, 200)
    # En ideal: dx1/dx2 = A2/A1 = r
    dx_ratio = r
    ax2.plot(r, dx_ratio)
    # punto actual
    current_dx_ratio = (dx1 / dx2) if dx2 != 0 else np.nan
    ax2.scatter([ratio_A], [current_dx_ratio])
    ax2.set_xlabel("A2/A1")
    ax2.set_ylabel("Δx1/Δx2")
    ax2.set_title("Relación de desplazamientos vs relación de áreas (ideal: y = x)")

st.pyplot(fig2)

# ---------- Coherencia dimensional (texto corto) ----------
with st.expander("Coherencia dimensional (para explicar en el video)"):
    st.write(
        "- Presión: P = F/A → N/m² (Pa)\n"
        "- Conservación de volumen: A·Δx → m²·m = m³\n"
        "- Trabajo: W = F·Δx → N·m = J\n"
    )