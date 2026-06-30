
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Dashboard")
st.caption("Resumen general del Sistema de Compras y Cuentas por Pagar")

# =======================
# KPIs (temporales)
# =======================

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Deuda Total", "S/ 0.00")
c2.metric("🧾 Facturas Pendientes", "0")
c3.metric("🏪 Proveedores", "0")
c4.metric("📦 Productos Importados", "0")

st.divider()

# =======================
# Datos demo
# =======================

df = pd.DataFrame({
    "Categoría": ["Legumbres", "Hierbas", "Frutas"],
    "Importe": [0, 0, 0]
})

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Compras por Categoría")

    fig = px.bar(
        df,
        x="Categoría",
        y="Importe",
        text="Importe"
    )

    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("⚠ Alertas")

    st.warning("No existen pedidos importados.")
    st.info("No existen compras registradas.")
    st.success("Sistema listo para comenzar.")

st.divider()

st.subheader("📋 Últimos Pedidos")

tabla = pd.DataFrame({
    "Fecha": [],
    "Categoría": [],
    "Productos": [],
    "Estado": []
})

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True,
    height=250
)

st.divider()

st.subheader("🚀 Accesos Rápidos")

a, b, c = st.columns(3)

with a:
    if st.button("📥 Importar Pedido", use_container_width=True):
        st.info("Seleccione 'Importar Excel' en el menú lateral.")

with b:
    if st.button("🏪 Proveedores", use_container_width=True):
        st.info("Módulo en desarrollo.")

with c:
    if st.button("💰 Cuentas por Pagar", use_container_width=True):
        st.info("Módulo en desarrollo.")
