import pandas as pd

HOJAS_VALIDAS = [
    "LEGUMBRES-PEDIDO",
    "HIERBAS-PEDIDO",
    "FRUTA-PEDIDO"
]


def leer_excel(file):

    excel = pd.ExcelFile(file)

    data = []

    for hoja in excel.sheet_names:

        if hoja not in HOJAS_VALIDAS:
            continue

        df = pd.read_excel(
            file,
            sheet_name=hoja,
            header=4
        )

        df.columns = df.columns.astype(str).str.strip()

        # -----------------------------
        # Buscar columnas importantes
        # -----------------------------

        producto = None
        costo = None

        for c in df.columns:

            nombre = c.upper()

            if "PRODUCTO" in nombre:
                producto = c

            if "COSTO" in nombre:
                costo = c

        if producto is None or costo is None:
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
            "U.M."
        ]

        for c in df.columns:

            nombre = c.upper()

            if any(x in nombre for x in ignorar):
                continue

            if "UNNAMED" in nombre:
                continue

            columnas_tiendas.append(c)

        # -----------------------------

        for _, fila in df.iterrows():

            if pd.isna(fila[producto]):
                continue

            registro = {}

            registro["Categoria"] = hoja.replace("-PEDIDO", "")

            registro["Producto"] = fila[producto]

            registro["Precio"] = fila[costo]

            total = 0

            for tienda in columnas_tiendas:

                try:
                    valor = float(fila[tienda])
                except:
                    valor = 0

                registro[tienda] = valor

                total += valor

            registro["Total Pedido"] = total

            data.append(registro)

    return pd.DataFrame(data)
