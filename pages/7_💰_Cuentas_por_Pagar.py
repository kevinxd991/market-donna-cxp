
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cuentas por Pagar",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cuentas por Pagar")
st.caption("Resumen de la deuda por proveedor")

if "facturas" not in st.session_state or st.session_state["facturas"].empty:
    st.warning("No existen facturas registradas.")
    st.stop()

facturas = st.session_state["facturas"].copy()

# Si aún no existe la columna Pagado la creamos
if "Pagado" not in facturas.columns:
    facturas["Pagado"] = 0.0

facturas["Saldo"] = facturas["Total"] - facturas["Pagado"]

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Deuda Total", f"S/ {facturas['Saldo'].sum():,.2f}")
c2.metric("🧾 Facturas", len(facturas))
c3.metric("🏪 Proveedores", facturas["Proveedor"].nunique())
c4.metric(
    "Pendientes",
    len(facturas[facturas["Saldo"] > 0])
)

st.divider()

buscar = st.text_input("🔍 Buscar proveedor")

tabla = facturas.copy()

if buscar:
    tabla = tabla[
        tabla["Proveedor"].astype(str).str.contains(
            buscar,
            case=False,
            na=False
        )
    ]

st.subheader("Facturas Pendientes")

mostrar = tabla[
    [
        "Proveedor",
        "Factura",
        "Fecha",
        "Total",
        "Pagado",
        "Saldo",
        "Estado"
    ]
]

st.dataframe(
    mostrar,
    use_container_width=True,
    hide_index=True,
    height=350
)

st.divider()

st.subheader("Resumen por Proveedor")

resumen = (
    tabla
    .groupby("Proveedor")
    .agg(
        Facturas=("Factura","count"),
        Total=("Total","sum"),
        Pagado=("Pagado","sum"),
        Saldo=("Saldo","sum")
    )
    .reset_index()
)

st.dataframe(
    resumen,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Detalle por proveedor")

for proveedor, grupo in tabla.groupby("Proveedor"):

    with st.expander(f"🏪 {proveedor}"):

        st.dataframe(
            grupo[
                [
                    "Factura",
                    "Fecha",
                    "Total",
                    "Pagado",
                    "Saldo",
                    "Estado"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

        st.metric(
            "Saldo Pendiente",
            f"S/ {grupo['Saldo'].sum():,.2f}"
        )

st.info(
    "En la siguiente versión, desde esta pantalla podrás registrar pagos parciales y totales. "
    "El saldo se actualizará automáticamente."
)
