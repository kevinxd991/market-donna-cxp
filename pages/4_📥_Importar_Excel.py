import streamlit as st
import pandas as pd

from utils.excel_reader import leer_excel

st.set_page_config(
    page_title="Importar Pedido",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Importar Pedido Diario")

st.caption("Carga el Excel generado diariamente para obtener los productos, precios y cantidades solicitadas.")

st.divider()

archivo = st.file_uploader(
    "Seleccione el archivo Excel",
    type=["xlsx"]
)

if archivo is not None:

    with st.spinner("Leyendo archivo..."):

        pedido = leer_excel(archivo)

    if pedido.empty:

        st.error("No se encontraron productos.")

        st.stop()

    # ---------------- KPIs ----------------

    productos = len(pedido)

    categorias = pedido["Categoria"].nunique()

    precio_promedio = pedido["Precio"].mean()

    total_productos = pedido["Total Pedido"].sum()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Productos",
        productos
    )

    c2.metric(
        "Categorías",
        categorias
    )

    c3.metric(
        "Precio Promedio",
        f"S/ {precio_promedio:.2f}"
    )

    c4.metric(
        "Cantidad Solicitada",
        f"{total_productos:,.2f}"
    )

    st.divider()

    # ---------------- BUSCADOR ----------------

    buscar = st.text_input(
        "🔍 Buscar producto"
    )

    tabla = pedido.copy()
    tabla = tabla.sort_values(
    by="Categoria"
)

    if buscar:

        tabla = tabla[
            tabla["Producto"]
            .str.contains(
                buscar,
                case=False,
                na=False
            )
        ]

    # ---------------- FILTRO ----------------

    categoria = st.selectbox(

        "Categoría",

        ["Todas"] + sorted(
            pedido["Categoria"].unique()
        )

    )

    if categoria != "Todas":

        tabla = tabla[
            tabla["Categoria"] == categoria
        ]

    st.divider()

    st.dataframe(

        tabla,

        use_container_width=True,

        hide_index=True,

        height=600

    )

    st.divider()

    col1,col2,col3 = st.columns([1,1,5])

    with col1:

        st.button(
            "💾 Guardar Pedido",
            use_container_width=True
        )

    with col2:

        csv = tabla.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(

            "📥 CSV",

            csv,

            "pedido.csv",

            "text/csv",

            use_container_width=True

        )
