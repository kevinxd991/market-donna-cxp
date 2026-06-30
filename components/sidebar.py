from streamlit_option_menu import option_menu
import streamlit as st


def sidebar():

    with st.sidebar:

        opcion = option_menu(

            menu_title="🏪 Market Donna ERP",

            options=[

                "Dashboard",

                "Importar Pedido",

                "Compras",

                "Proveedores",

                "Facturas",

                "Cuentas por Pagar",

                "Pagos",

                "Reportes",

                "Configuración"

            ],

            icons=[

                "house",

                "cloud-upload",

                "cart",

                "people",

                "file-earmark-text",

                "cash-stack",

                "credit-card",

                "bar-chart",

                "gear"

            ],

            default_index=0,

            styles={

                "container":{

                    "padding":"10px",

                    "background-color":"#fafafa"

                },

                "icon":{

                    "color":"#2563EB",

                    "font-size":"18px"

                },

                "nav-link":{

                    "font-size":"16px",

                    "text-align":"left",

                    "margin":"3px",

                    "border-radius":"8px"

                },

                "nav-link-selected":{

                    "background-color":"#2563EB",

                    "color":"white"

                }

            }

        )

    return opcion
