
import streamlit as st
import pandas as pd

from utils.excel_reader import (
    leer_excel,
    obtener_kpis,
    resumen_categoria,
    top_productos
)

st.set_page_config(
    page_title="Importar Pedido",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Importar Pedido Diario")
st.caption("Carga el Excel diario de Market Donna")

archivo = st.file_uploader(
    "Seleccione el archivo Excel",
    type=["xlsx"]
)

if archivo is None:
    st.info("Seleccione un archivo para comenzar.")
    st.stop()

with st.spinner("Leyendo archivo..."):
    pedido = leer_excel(archivo)

if pedido.empty:
    st.error("No se encontró información válida.")
    st.stop()

kpis = obtener_kpis(pedido)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Productos",kpis["productos"])
c2.metric("Categorías",kpis["categorias"])
c3.metric("Cantidad",f'{kpis["cantidad"]:,.2f}')
c4.metric("Importe",f'S/ {kpis["importe"]:,.2f}')

st.divider()

st.subheader("Resumen por categoría")
st.dataframe(
    resumen_categoria(pedido),
    use_container_width=True,
    hide_index=True
)

st.divider()

buscar = st.text_input("🔍 Buscar producto")

tabla = pedido.copy()

if buscar:
    tabla = tabla[
        tabla["Producto"].astype(str).str.contains(
            buscar,
            case=False,
            na=False
        )
    ]

categorias = ["Todas"] + sorted(tabla["Categoria"].unique().tolist())

categoria = st.selectbox(
    "Categoría",
    categorias
)

if categoria != "Todas":
    tabla = tabla[
        tabla["Categoria"] == categoria
    ]

st.divider()

tabs = st.tabs([
    "🥔 LEGUMBRES",
    "🌿 HIERBAS",
    "🍎 FRUTA"
])

mapa = {
    "🥔 LEGUMBRES":"LEGUMBRES",
    "🌿 HIERBAS":"HIERBAS",
    "🍎 FRUTA":"FRUTA"
}

for tab,nombre in zip(tabs,mapa.keys()):
    with tab:
        df = tabla[
            tabla["Categoria"] == mapa[nombre]
        ]

        if df.empty:
            st.warning("No hay registros.")
        else:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=450
            )

st.divider()

col1,col2 = st.columns([2,1])

with col1:
    st.subheader("Top productos solicitados")

    st.dataframe(
        top_productos(pedido)[
            ["Producto","Categoria","Precio","Total Pedido","Importe"]
        ],
        use_container_width=True,
        hide_index=True
    )

with col2:

    st.subheader("Acciones")

    if st.button(
        "💾 Guardar Pedido",
        use_container_width=True
    ):
        st.success(
            "Próximamente se guardará en la base de datos."
        )

    csv = pedido.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 Descargar CSV",
        csv,
        file_name="pedido_importado.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

st.success("✅ Pedido importado correctamente.")
