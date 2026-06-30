
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Productos",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Catálogo de Productos")
st.caption("Productos importados desde los pedidos diarios.")

if "pedido" in st.session_state:
    productos = (
        st.session_state["pedido"]
        .drop_duplicates(subset=["Producto"])
        .copy()
    )
else:
    productos = pd.DataFrame(columns=[
        "Categoria",
        "Producto",
        "Precio"
    ])

if "Proveedor Principal" not in productos.columns:
    productos["Proveedor Principal"] = ""

st.subheader("Resumen")

c1, c2, c3 = st.columns(3)

c1.metric("Productos", len(productos))
c2.metric(
    "Categorías",
    productos["Categoria"].nunique() if not productos.empty else 0
)
c3.metric(
    "Precio Promedio",
    f"S/ {productos['Precio'].mean():.2f}" if not productos.empty else "S/ 0.00"
)

st.divider()

buscar = st.text_input("🔍 Buscar producto")

tabla = productos.copy()

if buscar:
    tabla = tabla[
        tabla["Producto"].astype(str).str.contains(
            buscar,
            case=False,
            na=False
        )
    ]

categoria = st.selectbox(
    "Categoría",
    ["Todas"] + sorted(tabla["Categoria"].dropna().unique().tolist()) if not tabla.empty else ["Todas"]
)

if categoria != "Todas":
    tabla = tabla[tabla["Categoria"] == categoria]

st.subheader("Listado de productos")

editable = st.data_editor(
    tabla,
    column_config={
        "Proveedor Principal": st.column_config.TextColumn(
            "Proveedor Principal",
            help="Proveedor habitual del producto"
        )
    },
    disabled=[
        c for c in tabla.columns
        if c != "Proveedor Principal"
    ],
    hide_index=True,
    use_container_width=True,
    height=500
)

st.divider()

csv = editable.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "📥 Descargar Catálogo CSV",
    csv,
    file_name="catalogo_productos.csv",
    mime="text/csv",
    use_container_width=True
)

st.info(
    "En la siguiente etapa este catálogo se conectará con la base de datos para guardar el proveedor principal de cada producto y sugerirlo automáticamente al generar las compras."
)
