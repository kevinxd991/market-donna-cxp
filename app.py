import streamlit as st

st.set_page_config(
    page_title="Market Donna ERP",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CSS
# ============================

st.markdown("""
<style>

.block-container{
    padding-top:1.2rem;
}

h1{
    color:#1E3A8A;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    border:1px solid #E5E7EB;
    padding:18px;
    box-shadow:0px 2px 8px rgba(0,0,0,.08);
}

</style>
""",unsafe_allow_html=True)

# ============================

st.title("🏪 Market Donna ERP")

st.caption("Sistema Inteligente de Gestión de Compras y Cuentas por Pagar")

st.divider()

st.success("Bienvenido al sistema.")

st.markdown("""
Este sistema permitirá administrar:

- 📥 Importación automática del pedido diario
- 🏪 Proveedores
- 🛒 Compras
- 🧾 Facturas
- 💰 Cuentas por pagar
- 💳 Pagos
- 📊 Reportes

Seleccione un módulo desde el menú lateral.
""")

st.divider()

c1,c2,c3,c4=st.columns(4)

c1.metric("Productos","0")
c2.metric("Pedidos","0")
c3.metric("Proveedores","0")
c4.metric("Deuda","S/0.00")

st.info("Comience importando el pedido diario desde Excel.")
