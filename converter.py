"""
Esta script lee todos los archivos XLS de Cuenta Pública.
Los convierte en CSV, los une en uno solo y quita filas con
valores repetidos.

Fuente: https://www.cuentapublica.hacienda.gob.mx/

GC: Gasto corriente
GI: Gasto de Inversión
"""

import csv
import os

import pandas as pd
import xlrd


def convertir_archivos():
    """
    Iteramos sobre todos los archivos XLS.
    Algunos tienen un formato ligeramente diferente respecto a otros.

    Cada formato requiere una función diferente, ya que tienen diferentes columnas.
    """

    os.makedirs("./csv", exist_ok=True)

    for i in range(2013, 2023):
        if i <= 2014:
            procesar_archivo_antiguo_formato(i)
        else:
            procesar_archivo_nuevo_formato(i)

        print("Procesado:", i)


def procesar_archivo_antiguo_formato(archivo):
    """
    Procesa el archivo .xls usando las reglas para el antiguo formato (2013 y 2014).

    Parameters
    ==========
    archivo : str
        El año del archivo .xls

    """

    header = [
        "CICLO",
        "ENTE",
        "RAMO",
        "PROGRAMA",
        "PRESUPUESTO",
        "GC_SERVICIOS_PERSONALES",
        "GC_GASTO_DE_OPERACIÓN",
        "GC_SUBSIDIOS",
        "GC_OTROS_DE_CORRIENTE",
        "GC_SUMA",
        "GI_INVERSIÓN_FÍSICA",
        "GI_SUBSIDIOS",
        "GI_OTROS_DE_INVERSIÓN",
        "GI_SUMA",
        "TOTAL",
        "PORCENTAJE_CORRIENTE",
        "PORCENTAJE_INVERSIÓN",
    ]

    data_list = [header]

    book = xlrd.open_workbook(f"./xls/{archivo}.xls")
    sheet = book.sheet_by_index(0)

    latest_ente = ""
    latest_ramo = ""
    latest_programa = "TOTAL"

    for i in range(13, sheet.nrows - 1):
        valores = sheet.row_values(i)

        current_ente = valores[1].strip()
        current_ramo = valores[2].strip()
        current_programa = valores[3].strip()

        # Ente
        if current_ente != "":
            latest_ente = current_ente

        valores[1] = latest_ente

        # Ramo
        if current_ramo != "":
            latest_ramo = current_ramo

        valores[2] = latest_ramo

        # Programa
        if current_programa == "":
            # Revisamos el denominador.
            if valores[4] != "":
                valores[3] = latest_programa
            else:
                latest_programa = "TOTAL"
        else:
            latest_programa = current_programa
            valores[5] = latest_programa

        # Quitamos columnas vacías.
        valores.pop(5)
        valores = valores[1:]

        # Filtramos filas sin denominador.
        if valores[3] != "":
            data_list.append([archivo] + valores)

    with open(f"./csv/{archivo}.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows(data_list)


def procesar_archivo_nuevo_formato(archivo):
    """
    Procesa el archivo .xls usando las reglas para el nuevo formato (2015 en adelante).

    Parameters
    ==========
    archivo : str
        El año del archivo .xls

    """

    header = [
        "CICLO",
        "ENTE",
        "RAMO",
        "SUBRAMO",
        "PROGRAMA",
        "PRESUPUESTO",
        "GC_SERVICIOS_PERSONALES",
        "GC_GASTO_DE_OPERACIÓN",
        "GC_SUBSIDIOS",
        "GC_OTROS_DE_CORRIENTE",
        "GC_SUMA",
        "GI_PENSIONES_Y_JUBILACIONES",
        "GI_INVERSIÓN_FÍSICA",
        "GI_SUBSIDIOS",
        "GI_OTROS_DE_INVERSIÓN",
        "GI_SUMA",
        "TOTAL",
        "PORCENTAJE_CORRIENTE",
        "PORCENTAJE_PENSIONES_Y_JUBILACIONES",
        "PORCENTAJE_INVERSIÓN",
    ]

    # Quitamos jubilacón para el archivo del año 2015
    # ya que hasta el 2016 se empezaron a incluir eswas categorías.
    if archivo == 2015:
        header = [item for item in header if "JUBILACIONES" not in item]

    data_list = [header]

    book = xlrd.open_workbook(f"./xls/{archivo}.xls")
    sheet = book.sheet_by_index(0)

    latest_ente = ""
    latest_ramo = ""
    latest_subramo = ""
    latest_programa = "TOTAL"

    for i in range(9, sheet.nrows - 1):
        valores = sheet.row_values(i)

        current_ente = valores[2].strip()
        current_ramo = valores[3].strip()
        current_subramo = valores[4].strip()
        current_programa = valores[5].strip()

        # Ente
        if current_ente != "":
            latest_ente = current_ente
            latest_subramo = ""

        valores[2] = latest_ente

        # Ramo
        if current_ramo != "":
            latest_ramo = current_ramo

        valores[3] = latest_ramo

        # Subramo
        if current_subramo != "":
            latest_subramo = current_subramo

        valores[4] = latest_subramo

        # En ocasoines el ramo está en la columna del subramo.
        # Cuando sucede esto, lo acomodamos.
        if valores[3] == "" and valores[4] != "":
            valores[3] = valores[4]
            valores[4] = ""

        # Programa
        if current_programa == "":
            if valores[6] != "":
                valores[5] = latest_programa
            else:
                latest_programa = "TOTAL"
        else:
            latest_programa = current_programa
            valores[5] = latest_programa

        # Quitamos columnas vacías.
        valores = valores[2:]

        # Filtramos filas sin denominador.
        if valores[4] != "":
            data_list.append([archivo] + valores)

    with open(f"./csv/{archivo}.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows(data_list)


def compilar_archivos():
    """
    Compila todos los archivos CSV generados en uno solo.

    Se realizan algunas modificaciones para mantener la consistencia
    en todos los ciclos.
    """

    lista_df = list()

    for archivo in os.listdir("./csv"):
        df = pd.read_csv(f"./csv/{archivo}")
        lista_df.append(df)

    # Unimos todos los DataFrames en uno solo.
    final = pd.concat(lista_df)
    final = final.apply(fix_ramo, axis=1)

    # Actualizamos los nombres de ramos que han cambiado con el tiempo.
    final = final.replace(
        {
            "RAMO": {
                "Instituto Federal Electoral": "Instituto Nacional Electoral",
                "Comunicaciones y Transportes": "Infraestructura, Comunicaciones y Transportes",
                "Procuraduría General de la República": "Fiscalía General de la República",
                "Procuraduría General de la República (Ahora Fiscalía General de la República)": "Fiscalía General de la República",
                "Procuraduría General de la República (ahora Fiscalía General de la República)": "Fiscalía General de la República",
                "Agricultura, Ganadería, Desarrollo Rural, Pesca y Alimentación": "Agricultura y Desarrollo Rural",
                "Agricultura, Ganadería, Desarrollo Rural, Pesca y Alimentación (Ahora Agricultura y Desarrollo Rural)": "Agricultura y Desarrollo Rural",
                "Desarrollo Social": "Bienestar",
                "Desarrollo Social (Ahora Bienestar)": "Bienestar",
                "Instituto Nacional de Estadística y Geografía": "Información Nacional Estadística y Geográfica",
            }
        }
    )

    tipos = [
        "Aprobado",
        "Modificado",
        "Devengado",
        "Ejercicio",
        "Porcentaje Ejer/Aprob",
        "Porcentaje Ejer/Modif",
    ]

    # Vamos a crear una nueva columna llamada DESCRIPCIÓN, la cual
    # nos servirá para filtrar fácilmente algunos programas.
    final["DESCRIPCIÓN"] = final["PRESUPUESTO"]
    final["DESCRIPCIÓN"] = final["DESCRIPCIÓN"].apply(
        lambda x: None if x in tipos else x
    )
    final["DESCRIPCIÓN"] = final["DESCRIPCIÓN"].ffill(limit=6)

    # Quitamos las filas que son cabeceras, ya que estas no tienen valores númericos.
    final = final[final["DESCRIPCIÓN"] != final["PRESUPUESTO"]]

    # Quitamos las filas de porcentajes, esto es para reducir el tamaño
    # del archivo CSVO. Estos porcentajes se pueden recalcular fácilmente.
    final = final[
        ~final["PRESUPUESTO"].isin(["Porcentaje Ejer/Aprob", "Porcentaje Ejer/Modif"])
    ]

    # Quitamos las filas sin descripción, ya que estas contienen
    # valores repetidos de sus categorías padre.
    final = final[~pd.isna(final["DESCRIPCIÓN"])]

    final = final[final["PROGRAMA"] != "TOTAL"]

    columnas = [
        "CICLO",
        "ENTE",
        "RAMO",
        "PROGRAMA",
        "DESCRIPCIÓN",
        "PRESUPUESTO",
        "GC_SERVICIOS_PERSONALES",
        "GC_GASTO_DE_OPERACIÓN",
        "GC_SUBSIDIOS",
        "GC_OTROS_DE_CORRIENTE",
        "GC_SUMA",
        "GI_PENSIONES_Y_JUBILACIONES",
        "GI_INVERSIÓN_FÍSICA",
        "GI_SUBSIDIOS",
        "GI_OTROS_DE_INVERSIÓN",
        "GI_SUMA",
        "TOTAL",
        "PORCENTAJE_CORRIENTE",
        "PORCENTAJE_PENSIONES_Y_JUBILACIONES",
        "PORCENTAJE_INVERSIÓN",
    ]

    # Quitamos la columna de SUBRAMO y ordenamos el resto de columnas.
    final = final[columnas]

    # Finalmente guardamos el archivo a un nuevo CSV.
    final.to_csv("./data.csv", index=False, encoding="utf-8")


def compilar_totales():
    """
    Compila todos los archivos CSV generados en uno solo.

    Se realizan algunas modificaciones para mantener la consistencia
    en todos los ciclos.

    A diferencia de la otra función, el resultado de este archivo solo incluye
    los totales, haciendo que el archivo final sea aún más comapacto.
    """

    lista_df = list()

    for archivo in os.listdir("./csv"):
        df = pd.read_csv(f"./csv/{archivo}")
        lista_df.append(df)

    # Unimos todos los DataFrames en uno solo.
    final = pd.concat(lista_df)
    final = final.apply(fix_ramo, axis=1)

    # Actualizamos los nombres de ramos que han cambiado con el tiempo.
    final = final.replace(
        {
            "RAMO": {
                "Instituto Federal Electoral": "Instituto Nacional Electoral",
                "Comunicaciones y Transportes": "Infraestructura, Comunicaciones y Transportes",
                "Procuraduría General de la República": "Fiscalía General de la República",
                "Procuraduría General de la República (Ahora Fiscalía General de la República)": "Fiscalía General de la República",
                "Procuraduría General de la República (ahora Fiscalía General de la República)": "Fiscalía General de la República",
                "Agricultura, Ganadería, Desarrollo Rural, Pesca y Alimentación": "Agricultura y Desarrollo Rural",
                "Agricultura, Ganadería, Desarrollo Rural, Pesca y Alimentación (Ahora Agricultura y Desarrollo Rural)": "Agricultura y Desarrollo Rural",
                "Desarrollo Social": "Bienestar",
                "Desarrollo Social (Ahora Bienestar)": "Bienestar",
                "Instituto Nacional de Estadística y Geografía": "Información Nacional Estadística y Geográfica",
            }
        }
    )

    tipos = [
        "Aprobado",
        "Modificado",
        "Devengado",
        "Ejercicio",
        "Porcentaje Ejer/Aprob",
        "Porcentaje Ejer/Modif",
    ]

    # Vamos a crear una nueva columna llamada DESCRIPCIÓN, la cual
    # nos servirá para filtrar fácilmente algunos programas.
    final["DESCRIPCIÓN"] = final["PRESUPUESTO"]
    final["DESCRIPCIÓN"] = final["DESCRIPCIÓN"].apply(
        lambda x: None if x in tipos else x
    )
    final["DESCRIPCIÓN"] = final["DESCRIPCIÓN"].ffill(limit=6)

    # Quitamos las filas que son cabeceras, ya que estas no tienen valores númericos.
    final = final[final["DESCRIPCIÓN"] != final["PRESUPUESTO"]]

    # Quitamos las filas de porcentajes, esto es para reducir el tamaño
    # del archivo CSVO. Estos porcentajes se pueden recalcular fácilmente.
    final = final[
        ~final["PRESUPUESTO"].isin(["Porcentaje Ejer/Aprob", "Porcentaje Ejer/Modif"])
    ]

    # Quitamos las filas sin ramo, ya que estas contienen
    # valores repetidos de sus categorías padre.
    final = final[~pd.isna(final["RAMO"])]

    final = final[final["PROGRAMA"] == "TOTAL"]

    columnas = [
        "CICLO",
        "ENTE",
        "RAMO",
        "PRESUPUESTO",
        "GC_SERVICIOS_PERSONALES",
        "GC_GASTO_DE_OPERACIÓN",
        "GC_SUBSIDIOS",
        "GC_OTROS_DE_CORRIENTE",
        "GC_SUMA",
        "GI_PENSIONES_Y_JUBILACIONES",
        "GI_INVERSIÓN_FÍSICA",
        "GI_SUBSIDIOS",
        "GI_OTROS_DE_INVERSIÓN",
        "GI_SUMA",
        "TOTAL",
        "PORCENTAJE_CORRIENTE",
        "PORCENTAJE_PENSIONES_Y_JUBILACIONES",
        "PORCENTAJE_INVERSIÓN",
    ]

    # Quitamos la columna de SUBRAMO y ordenamos el resto de columnas.
    final = final[columnas]

    # Finalmente guardamos el archivo a un nuevo CSV.
    final.to_csv("./data_total.csv", index=False, encoding="utf-8")


def fix_ramo(x):
    """
    Esta función mueve el contenido de RAMO a ENTE y de SUBRAMO a RAMO
    solo en las filas donde el ENTE sea Poder Ejecutivo.

    Esto es con el propósito de que sea consistente en todos los ciclos.
    """

    if x["ENTE"] == "Poder Ejecutivo":
        x["ENTE"] = x["RAMO"]
        x["RAMO"] = x["SUBRAMO"]

        return x
    else:
        return x


if __name__ == "__main__":
    convertir_archivos()
    compilar_archivos()
    compilar_totales()
