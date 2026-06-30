
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Facturas",
    page_icon="🧾",
    layout="wide"
)

st.title("🧾 Registro de Facturas")
st.caption("Registre las facturas entregadas por los proveedores.")

# Base temporal
if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=[
        "Proveedor",
        "Factura",
        "Fecha",
        "Total",
        "Estado",
        "Observación"
    ])

# Lista de proveedores
if "proveedores" in st.session_state:
    proveedores_df = st.session_state["proveedores"]
    proveedores = proveedores_df["Nombre"].tolist()
else:
    proveedores = ["Mercado Santa Anita", "Juan Pérez", "Carlos Gómez"]

st.subheader("Nueva Factura")

with st.form("form_factura", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        proveedor = st.selectbox("Proveedor", proveedores)
        numero = st.text_input("Número de Factura")

    with col2:
        fecha = st.date_input("Fecha", value=date.today())
        total = st.number_input("Total (S/)", min_value=0.0, step=0.10)

    observacion = st.text_area("Observación")

    comprobante = st.file_uploader(
        "Adjuntar factura (PDF o imagen)",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    guardar = st.form_submit_button("💾 Registrar Factura")

if guardar:

    if numero.strip() == "":
        st.error("Ingrese el número de factura.")
        st.stop()

    existe = (
        (st.session_state["facturas"]["Proveedor"] == proveedor) &
        (st.session_state["facturas"]["Factura"] == numero)
    ).any()

    if existe:
        st.error("⚠ Esta factura ya fue registrada para este proveedor.")
        st.stop()

    nueva = pd.DataFrame([{
        "Proveedor": proveedor,
        "Factura": numero,
        "Fecha": fecha.strftime("%d/%m/%Y"),
        "Total": total,
        "Estado": "Pendiente",
        "Observación": observacion
    }])

    st.session_state["facturas"] = pd.concat(
        [st.session_state["facturas"], nueva],
        ignore_index=True
    )

    st.success("✅ Factura registrada correctamente.")

st.divider()

st.subheader("Facturas Registradas")

buscar = st.text_input("🔍 Buscar factura o proveedor")

tabla = st.session_state["facturas"].copy()

if buscar:
    filtro = (
        tabla["Proveedor"].astype(str).str.contains(buscar, case=False, na=False)
        |
        tabla["Factura"].astype(str).str.contains(buscar, case=False, na=False)
    )
    tabla = tabla[filtro]

st.dataframe(
    tabla,
    hide_index=True,
    use_container_width=True,
    height=350
)

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("Facturas", len(st.session_state["facturas"]))
c2.metric(
    "Pendientes",
    len(st.session_state["facturas"][st.session_state["facturas"]["Estado"] == "Pendiente"])
)
c3.metric(
    "Total",
    f"S/ {st.session_state['facturas']['Total'].sum():,.2f}"
)

st.info("En el siguiente módulo (Cuentas por Pagar) estas facturas se agruparán por proveedor y se calculará el saldo pendiente.")
