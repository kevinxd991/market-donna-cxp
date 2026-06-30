
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Generador de Compras",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Generador de Compras")
st.caption("Agrupa automáticamente los productos por proveedor.")

if "pedido" not in st.session_state:
    st.warning("Primero importa un pedido desde 'Importar Excel'.")
    st.stop()

pedido = st.session_state["pedido"].copy()

proveedores_demo = [
    "Mercado Santa Anita",
    "Juan Pérez",
    "Carlos Gómez",
    "Verduras SAC",
    "Frutas del Norte",
    "Sin asignar"
]

if "Proveedor" not in pedido.columns:
    pedido["Proveedor"] = "Sin asignar"

st.subheader("Asignación de proveedores")

col1, col2 = st.columns([2,1])

with col1:
    buscar = st.text_input("🔍 Buscar producto")

with col2:
    categoria = st.selectbox(
        "Categoría",
        ["Todas"] + sorted(pedido["Categoria"].unique().tolist())
    )

tabla = pedido.copy()

if buscar:
    tabla = tabla[
        tabla["Producto"].astype(str).str.contains(
            buscar,
            case=False,
            na=False
        )
    ]

if categoria != "Todas":
    tabla = tabla[
        tabla["Categoria"] == categoria
    ]

editable = st.data_editor(
    tabla,
    column_config={
        "Proveedor": st.column_config.SelectboxColumn(
            "Proveedor",
            options=proveedores_demo,
            required=True
        )
    },
    disabled=[c for c in tabla.columns if c != "Proveedor"],
    hide_index=True,
    use_container_width=True,
    height=500
)

# Actualizar pedido completo
pedido_actualizado = pedido.copy()
for _, fila in editable.iterrows():
    idx = pedido_actualizado["Producto"] == fila["Producto"]
    pedido_actualizado.loc[idx, "Proveedor"] = fila["Proveedor"]

st.session_state["pedido"] = pedido_actualizado

st.divider()

c1,c2,c3,c4 = st.columns(4)

c1.metric("Productos", len(pedido_actualizado))
c2.metric("Proveedores asignados",
          pedido_actualizado[pedido_actualizado["Proveedor"]!="Sin asignar"]["Proveedor"].nunique())
c3.metric("Sin asignar",
          len(pedido_actualizado[pedido_actualizado["Proveedor"]=="Sin asignar"]))
c4.metric("Importe",
          f'S/ {pedido_actualizado["Importe"].sum():,.2f}')

st.divider()

if st.button("📦 Generar Compras", use_container_width=True):

    compras = pedido_actualizado[
        pedido_actualizado["Proveedor"] != "Sin asignar"
    ]

    if compras.empty:
        st.error("Debe asignar al menos un proveedor.")
        st.stop()

    st.success("Compras generadas correctamente.")

    resumen = (
        compras
        .groupby("Proveedor")
        .agg(
            Productos=("Producto","count"),
            Cantidad=("Total Pedido","sum"),
            Importe=("Importe","sum")
        )
        .reset_index()
    )

    st.subheader("📋 Resumen por proveedor")
    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    for proveedor, grupo in compras.groupby("Proveedor"):

        with st.expander(f"🏪 {proveedor}", expanded=False):

            mostrar = grupo[
                [
                    "Categoria",
                    "Producto",
                    "Precio",
                    "Total Pedido",
                    "Importe"
                ]
            ]

            st.dataframe(
                mostrar,
                hide_index=True,
                use_container_width=True
            )

            st.metric(
                "Total Compra",
                f'S/ {grupo["Importe"].sum():,.2f}'
            )

    st.session_state["compras_generadas"] = compras

    csv = compras.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📥 Descargar Compras CSV",
        csv,
        file_name="compras_generadas.csv",
        mime="text/csv",
        use_container_width=True
    )
