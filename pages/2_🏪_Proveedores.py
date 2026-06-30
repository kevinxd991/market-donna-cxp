
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Proveedores",
    page_icon="🏪",
    layout="wide"
)

st.title("🏪 Proveedores")
st.caption("Administración de proveedores (modo demostración)")

if "proveedores" not in st.session_state:
    st.session_state["proveedores"] = pd.DataFrame([
        {
            "Nombre":"Mercado Santa Anita",
            "RUC":"",
            "Contacto":"",
            "Teléfono":"",
            "Días Crédito":7,
            "Estado":"Activo"
        }
    ])

proveedores = st.session_state["proveedores"]

st.subheader("➕ Registrar proveedor")

with st.form("nuevo_proveedor", clear_on_submit=True):

    c1,c2 = st.columns(2)

    with c1:
        nombre = st.text_input("Nombre")
        ruc = st.text_input("RUC")
        contacto = st.text_input("Contacto")

    with c2:
        telefono = st.text_input("Teléfono")
        credito = st.number_input("Días de crédito",0,365,0)
        estado = st.selectbox("Estado",["Activo","Inactivo"])

    guardar = st.form_submit_button("💾 Guardar proveedor")

if guardar:
    if nombre.strip()=="":
        st.error("Ingrese el nombre del proveedor.")
    else:
        nuevo = pd.DataFrame([{
            "Nombre":nombre,
            "RUC":ruc,
            "Contacto":contacto,
            "Teléfono":telefono,
            "Días Crédito":credito,
            "Estado":estado
        }])
        st.session_state["proveedores"] = pd.concat(
            [st.session_state["proveedores"], nuevo],
            ignore_index=True
        )
        st.success("Proveedor registrado.")
        st.rerun()

st.divider()

st.subheader("📋 Lista de proveedores")

buscar = st.text_input("🔍 Buscar proveedor")

tabla = st.session_state["proveedores"].copy()

if buscar:
    tabla = tabla[
        tabla["Nombre"].str.contains(
            buscar,
            case=False,
            na=False
        )
    ]

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True,
    height=350
)

st.divider()

c1,c2,c3 = st.columns(3)

c1.metric("Proveedores", len(st.session_state["proveedores"]))
c2.metric("Activos",
          len(st.session_state["proveedores"][st.session_state["proveedores"]["Estado"]=="Activo"]))
c3.metric("Inactivos",
          len(st.session_state["proveedores"][st.session_state["proveedores"]["Estado"]=="Inactivo"]))

st.info("Más adelante este módulo se conectará con Supabase y mostrará compras, facturas, saldo pendiente e historial de pagos por proveedor.")
