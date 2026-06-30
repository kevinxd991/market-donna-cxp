import pandas as pd

HOJAS_VALIDAS = [
    "LEGUMBRES-PEDIDO",
    "HIERBAS-PEDIDO",
    "FRUTA-PEDIDO"
]


def leer_excel(file):

    pedidos=[]

    excel=pd.ExcelFile(file)

    hojas=[h for h in excel.sheet_names if h in HOJAS_VALIDAS]

    for hoja in hojas:

        df=pd.read_excel(
            file,
            sheet_name=hoja,
            header=4
        )

        df.columns=df.columns.astype(str).str.strip()

        columnas=list(df.columns)

        producto=None
        costo=None

        for c in columnas:

            texto=c.upper()

            if "PRODUCTO" in texto:
                producto=c

            if "COSTO" in texto:
                costo=c

        if producto is None:
            continue

        if costo is None:
            continue

        columnas_pedido=[]

        ignorar=[
            "PRODUCTO",
            "COSTO",
            "CODIGO",
            "CÓDIGO",
            "U.M.",
            "TOTAL"
        ]

        for c in columnas:

            nombre=c.upper()

            if any(x in nombre for x in ignorar):
                continue

            if "Unnamed" in c:
                continue

            columnas_pedido.append(c)

        for _,fila in df.iterrows():

            if pd.isna(fila[producto]):
                continue

            total=0

            for col in columnas_pedido:

                try:
                    valor=float(fila[col])

                except:
                    valor=0

                total+=valor

            pedidos.append({

                "Categoria":hoja.replace("-PEDIDO",""),

                "Producto":fila[producto],

                "Precio":fila[costo],

                "Pedido":total

            })

    return pd.DataFrame(pedidos)
