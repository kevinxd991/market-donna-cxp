import pandas as pd

# ==========================================
# HOJAS QUE SE IMPORTARÁN
# ==========================================

HOJAS_VALIDAS = [
    "LEGUMBRES-PEDIDO",
    "HIERBAS-PEDIDO",
    "FRUTA-PEDIDO"
]


def leer_excel(archivo):
    """
    Lee el Excel de pedidos y devuelve un DataFrame unificado.
    """

    excel = pd.ExcelFile(archivo)

    datos = []

    for hoja in excel.sheet_names:

        if hoja not in HOJAS_VALIDAS:
            continue

        try:

            df = pd.read_excel(
                archivo,
                sheet_name=hoja,
                header=4
            )

        except Exception:
            continue

        # -----------------------------
        # Limpiar nombres de columnas
        # -----------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # -----------------------------
        # Buscar columnas principales
        # -----------------------------

        columna_producto = None
        columna_precio = None

        for columna in df.columns:

            if "PRODUCTO" in columna:
                columna_producto = columna

            if "COSTO" in columna:
                columna_precio = columna

        if columna_producto is None:
            continue

        if columna_precio is None:
            continue

        # -----------------------------
        # Detectar columnas de tiendas
        # -----------------------------

        columnas_tiendas = []

        ignorar = [
            "CODIGO",
            "CÓDIGO",
            "PRODUCTO",
            "COSTO",
            "TOTAL",
            "U.M.",
            "UM"
        ]

        for columna in df.columns:

            nombre = columna.upper()

            if any(x in nombre for x in ignorar):
                continue

            if "UNNAMED" in nombre:
                continue

            columnas_tiendas.append(columna)

        # -----------------------------
        # Recorrer productos
        # -----------------------------

        for _, fila in df.iterrows():

            producto = fila[columna_producto]

            if pd.isna(producto):
                continue

            if str(producto).strip() == "":
                continue

            registro = {}

            registro["Categoria"] = hoja.replace("-PEDIDO", "")

            registro["Producto"] = str(producto).strip()

            try:
                registro["Precio"] = float(fila[columna_precio])
            except:
                registro["Precio"] = 0

            total = 0

            # Guardar cantidad por tienda

            for tienda in columnas_tiendas:

                try:
                    cantidad = float(fila[tienda])

                    if pd.isna(cantidad):
                        cantidad = 0

                except:
                    cantidad = 0

                registro[tienda.title()] = cantidad

                total += cantidad

            registro["Total Pedido"] = total

            registro["Importe"] = round(
                total * registro["Precio"],
                2
            )

            datos.append(registro)

    if len(datos) == 0:
        return pd.DataFrame()

    pedido = pd.DataFrame(datos)

    pedido = pedido.fillna(0)

    pedido = pedido.sort_values(
        ["Categoria", "Producto"]
    )

    pedido.reset_index(
        drop=True,
        inplace=True
    )

    return pedido


# ==========================================
# KPIs
# ==========================================

def obtener_kpis(df):

    if df.empty:

        return {
            "productos": 0,
            "categorias": 0,
            "cantidad": 0,
            "importe": 0
        }

    return {

        "productos": len(df),

        "categorias": df["Categoria"].nunique(),

        "cantidad": df["Total Pedido"].sum(),

        "importe": df["Importe"].sum()

    }


# ==========================================
# RESUMEN POR CATEGORÍA
# ==========================================

def resumen_categoria(df):

    if df.empty:
        return pd.DataFrame()

    return (

        df.groupby("Categoria")

        .agg(

            Productos=("Producto", "count"),

            Cantidad=("Total Pedido", "sum"),

            Importe=("Importe", "sum")

        )

        .reset_index()

    )


# ==========================================
# TOP PRODUCTOS
# ==========================================

def top_productos(df, cantidad=10):

    if df.empty:
        return pd.DataFrame()

    return (

        df

        .sort_values(
            "Total Pedido",
            ascending=False
        )

        .head(cantidad)

    )
