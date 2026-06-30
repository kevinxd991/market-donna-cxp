import streamlit as st

# ---------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------

st.set_page_config(
    page_title="Market Donna ERP",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CSS PERSONALIZADO
# ---------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}

h1,h2,h3{
    color:#1f2937;
}

div[data-testid="stMetric"]{
    background-color:white;
    border:1px solid #E5E7EB;
    padding:18px;
    border-radius:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------

col1,col2 = st.columns([1,6])

with col1:
    st.image(
        "https://img.icons8.com/color/96/shop.png",
        width=70
    )

with col2:

    st.title("🏪 Market Donna ERP")

    st.caption(
        "Sistema de Gestión de Compras y Cuentas por Pagar a Proveedores"
    )

st.divider()

# ---------------------------------------------------
# MENSAJE DE BIENVENIDA
# ---------------------------------------------------

st.success("✅ Bienvenido al sistema.")

st.write("""

Este sistema permitirá administrar:

- 🏪 Proveedores
- 📦 Productos
- 📥 Importación de pedidos desde Excel
- 🛒 Compras
- 🧾 Facturas
- 💰 Cuentas por pagar
- 💳 Pagos
- 📊 Reportes

Utilice el menú lateral para acceder a cada módulo.

""")

st.divider()

# ---------------------------------------------------
# KPIs TEMPORALES
# ---------------------------------------------------

st.subheader("Resumen General")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Deuda Total",
        "S/ 0.00"
    )

with col2:
    st.metric(
        "🧾 Facturas Pendientes",
        "0"
    )

with col3:
    st.metric(
        "💳 Pagado este mes",
        "S/ 0.00"
    )

with col4:
    st.metric(
        "🏪 Proveedores",
        "0"
    )

st.divider()

st.info("📌 Próximamente aquí se mostrará el Dashboard con gráficos en tiempo real.")
