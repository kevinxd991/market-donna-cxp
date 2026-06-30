
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Generar Compras",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Generar Compras")
st.caption("Asigna un proveedor a cada producto importado.")

if "pedido" not in st.session_state:
    st.warning("Primero importa un pedido desde el módulo 'Importar Excel'.")
    st.stop()

pedido = st.session_state["pedido"].copy()

proveedores_demo = [
    "Sin asignar",
    "Juan Pérez",
    "Carlos Gómez",
    "Mercado Santa Anita",
    "Proveedor General"
]

st.info("Esta pantalla usa proveedores de ejemplo. Más adelante se conectará a la base de datos.")

if "Proveedor" not in pedido.columns:
    pedido["Proveedor"] = "Sin asignar"

st.subheader("Asignación de proveedores")

editado = st.data_editor(
    pedido,
    column_config={
        "Proveedor": st.column_config.SelectboxColumn(
            "Proveedor",
            options=proveedores_demo,
            required=True,
        )
    },
    disabled=[c for c in pedido.columns if c != "Proveedor"],
    hide_index=True,
    use_container_width=True,
    num_rows="fixed"
)

st.session_state["pedido"] = editado

st.divider()

if st.button("📦 Generar Compras", use_container_width=True):

    compras = editado[editado["Proveedor"] != "Sin asignar"].copy()

    if compras.empty:
        st.error("Debe asignar al menos un proveedor.")
        st.stop()

    st.success("Compras generadas correctamente.")

    for proveedor, grupo in compras.groupby("Proveedor"):

        st.markdown(f"## 🏪 {proveedor}")

        columnas = [c for c in [
            "Producto",
            "Precio",
            "Total Pedido",
            "Importe"
        ] if c in grupo.columns]

        st.dataframe(
            grupo[columnas],
            hide_index=True,
            use_container_width=True
        )

        if "Importe" in grupo.columns:
            total = grupo["Importe"].sum()
            st.metric("Total Compra", f"S/ {total:,.2f}")

        st.divider()

    st.session_state["compras_generadas"] = compras
