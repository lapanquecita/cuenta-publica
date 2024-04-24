"""
Este script contiene ejemplos de como usar la base de datos
de Cuenta Pública creada en converter.py
"""

import pandas as pd
import plotly.graph_objects as go


def main():
    """
    Esta función compara cifras anuales de distintos ramos / programas.
    """

    # Cargamos el dataset que contiene la información de todoslos archivos XLS.
    df = pd.read_csv("./data.csv")

    # Seleccioamos los registros del año 2019 al 2022.
    df = df[df["CICLO"].between(2019, 2022)]

    # Seleccionamos las cifras de presupuesto ejercido.
    df = df[df["PRESUPUESTO"] == "Ejercicio"]

    # Seleccionamos las cifras del ramo: INAI.
    inai = (
        df[
            df["RAMO"]
            == "Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales"
        ]
        .groupby("CICLO")
        .sum()["TOTAL"]
        / 1000000
    )

    # Seleccionamos las cifras del ramo: INE.
    ine = (
        df[df["RAMO"] == "Instituto Nacional Electoral"].groupby("CICLO").sum()["TOTAL"]
        / 1000000
    )

    # Seleccionamos las cifras del programa: Jóvenes Cosnstruyendo el Futuro.
    jovenes = (
        df[df["DESCRIPCIÓN"] == "Jóvenes Construyendo el Futuro"]
        .groupby("CICLO")
        .sum()["TOTAL"]
        / 1000000
    )

    # Vamos a crear 3 gráficas de barras verticales para
    # comparar los valores anuales de cada categoría.
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=inai.index,
            y=inai.values,
            text=inai.values,
            texttemplate="%{text:,.0f}",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=26,
            textposition="outside",
            name="Instituto Nacional de Acceso a la Información",
            marker_color="#5D69B1",
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.add_trace(
        go.Bar(
            x=ine.index,
            y=ine.values,
            text=ine.values,
            texttemplate="%{text:,.0f}",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=26,
            textposition="outside",
            name="Instituto Nacional Electoral",
            marker_color="#52BCA3",
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.add_trace(
        go.Bar(
            x=jovenes.index,
            y=jovenes.values,
            text=jovenes.values,
            texttemplate="%{text:,.0f}",
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=26,
            textposition="outside",
            name="Jóvenes Construyendo el Futuro",
            marker_color="#E58606",
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.update_xaxes(
        tickformat="%m<br>'%y",
        ticks="outside",
        tickfont_size=14,
        ticklen=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        gridwidth=0.6,
        mirror=True,
    )

    fig.update_yaxes(
        range=[0, 33000],
        title="Millones de pesos (nominales)",
        tickfont_size=16,
        separatethousands=True,
        ticks="outside",
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.6,
        showline=True,
        mirror=True,
        nticks=14,
    )

    fig.update_layout(
        legend_itemsizing="constant",
        legend_font_size=14,
        showlegend=True,
        legend_x=0.98,
        legend_y=0.98,
        legend_xanchor="right",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Lato",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Comparación del presupuesto anual ejercido del INAI, INE y Jóvenes Construyendo el Futuro (2019-2022)",
        title_x=0.5,
        title_y=0.97,
        margin_t=60,
        margin_l=110,
        margin_r=40,
        margin_b=80,
        title_font_size=22,
        plot_bgcolor="#111111",
        paper_bgcolor="#282A3A",
        annotations=[
            dict(
                x=0.5,
                y=0.92,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                bordercolor="#FFFFFF",
                borderwidth=1.5,
                borderpad=6,
                font_size=14,
                bgcolor="#111111",
                text=f"<b>Nota:</b> Incluye gastos corrientes y de inversión.",
            ),
            dict(
                x=0.01,
                y=-0.12,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: SHCP (Cuenta Pública 2013-2022)",
            ),
            dict(
                x=0.5,
                y=-0.12,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año fiscal",
            ),
            dict(
                x=1.01,
                y=-0.12,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./comparacion_anual.png")


def main2():
    graficar_programa(
        "vacuna", "Programa de Vacunación", "#5D69B1", "#E58606", "left", 1
    )

    graficar_programa(
        "vigilancia epidemiológica",
        "Programa de Vigilancia Epidemiológica",
        "#ED645A",
        "#2F8AC4",
        "right",
        2,
    )

    graficar_ramo(
        "Bienestar",
        "Secretaría del Bienestar (Desarrollo Social)",
        "#DAA51B",
        "#24796C",
        "left",
        3,
    )

    graficar_ramo(
        "Consejo Nacional de Ciencia y Tecnología",
        "CONACyT",
        "#764E9F",
        "#52BCA3",
        "right",
        4,
    )

    graficar_ramo(
        "Trabajo y Previsión Social",
        "Secretaría del Trabajo y Previsión Social",
        "#3949ab",
        "#ff3d00",
        "left",
        5,
    )

    graficar_ramo("Turismo", "Secretaría del Turismo", "#ffa000", "#689f38", "left", 6)


def graficar_programa(nombre, titulo, color1, color2, pos, archivo):
    """
    Esta función crea gráficas de barras con el nombre del programa especificado.
    Las cifras se ajustan por inflación usando el Índice de Precios al Consumidor.
    """

    # Cargamos el dataset de IPC.
    ipc = pd.read_csv("./assets/IPC.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Este IPC será nuestro valor de referencia.
    # El valor puede cambiar con el tiempo.
    ipc_referencia = ipc["IPC"].iloc[-1]

    # Si queremos usar el IPC de enero usamos first()
    # Si queremos usar el IPC de diciembre usamos last()
    ipc = ipc.resample("YS").last()

    # CAlculamos el factor.
    ipc["FACTOR"] = ipc_referencia / ipc["IPC"]

    # Solo necesitamos el año del IPC.
    ipc.index = ipc.index.year

    # Cargamos el dataset de Cuenta Pública.
    df = pd.read_csv("./data.csv")

    # Filtramos nuestro DataFrame con el programa especificado.
    final = df[df["DESCRIPCIÓN"].str.contains(nombre, case=False)]

    final = (
        final.pivot_table(
            index="CICLO", columns="PRESUPUESTO", values="TOTAL", aggfunc="sum"
        )
        / 1000000
    )

    # Ajustamos las cifras por la inflación.
    final["Aprobado_Ajustado"] = final["Aprobado"] * ipc["FACTOR"]
    final["Ejercicio_Ajustado"] = final["Ejercicio"] * ipc["FACTOR"]

    # Creamos los textos para las cifras ajustadas.
    final["Aprobado_Ajustado_Texto"] = final["Aprobado_Ajustado"].apply(abreviar_cifra)
    final["Ejercicio_Ajustado_Texto"] = final["Ejercicio_Ajustado"].apply(
        abreviar_cifra
    )

    # Vamos a crear una tabla con los porcentajes anuales.
    tabla = "<b>Ejercido/Aprobado</b>"

    for k, v in final.iterrows():
        try:
            tabla += f"<br>{k}: {(v['Ejercicio_Ajustado'] / v['Aprobado_Ajustado']) * 100:,.2f}%"
        except:
            # En algunos casos el monto aprobado es 0.
            tabla += f"<br>{k}: ---"

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=final.index,
            y=final["Aprobado_Ajustado"],
            text=final["Aprobado_Ajustado_Texto"],
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=18,
            textposition="outside",
            name="Aprobado",
            marker_color=color1,
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.add_trace(
        go.Bar(
            x=final.index,
            y=final["Ejercicio_Ajustado"],
            text=final["Ejercicio_Ajustado_Texto"],
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=18,
            textposition="outside",
            name="Ejercido",
            marker_color=color2,
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.update_xaxes(
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    # Vamos a crer el rango para el eje vertical.
    maximo_aprobado = final["Aprobado_Ajustado"].max()
    maximo_ejercido = final["Ejercicio_Ajustado"].max()

    nuevo_maximo = (
        maximo_aprobado if maximo_aprobado >= maximo_ejercido else maximo_ejercido
    )

    fig.update_yaxes(
        range=[0, nuevo_maximo * 1.08],
        title="Millones de pesos a precios constantes de marzo de 2024",
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    # Acomodamos la tabla.
    if pos == "left":
        tabla_x = 0.02
        tabla_xanchor = "left"
    elif pos == "right":
        tabla_x = 0.995
        tabla_xanchor = "right"

    fig.update_layout(
        legend_orientation="h",
        legend_itemsizing="constant",
        showlegend=True,
        legend_x=0.5,
        legend_y=1.08,
        legend_xanchor="center",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=18,
        title_text=f"Evolución del gasto total anual del <b>{titulo}</b> en México",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=90,
        margin_l=120,
        margin_r=40,
        margin_b=90,
        plot_bgcolor="#111111",
        paper_bgcolor="#282A3A",
        annotations=[
            dict(
                x=tabla_x,
                y=0.92,
                xref="paper",
                yref="paper",
                xanchor=tabla_xanchor,
                yanchor="top",
                bordercolor="#FFFFFF",
                borderwidth=1.5,
                borderpad=7,
                bgcolor="#111111",
                align="left",
                font_size=12,
                text=tabla,
            ),
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: SHCP (Cuenta Pública 2013-2022)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año fiscal",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image(f"./{archivo}.png")


def graficar_ramo(nombre, titulo, color1, color2, pos, archivo):
    """
    Esta función crea gráficas de barras con el nombre del ramo especificado.
    Las cifras se ajustan por inflación usando el Índice de Precios al Consumidor.
    """

    # Cargamos el dataset de IPC.
    ipc = pd.read_csv("./assets/IPC.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Este IPC será nuestro valor de referencia.
    # El valor puede cambiar con el tiempo.
    ipc_referencia = ipc["IPC"].iloc[-1]

    # Si queremos usar el IPC de enero usamos first()
    # Si queremos usar el IPC de diciembre usamos last()
    ipc = ipc.resample("YS").last()

    # CAlculamos el factor.
    ipc["FACTOR"] = ipc_referencia / ipc["IPC"]

    # Solo necesitamos el año del IPC.
    ipc.index = ipc.index.year

    # Cargamos el dataset de los totales de Cuenta Pública.
    df = pd.read_csv("./data_total.csv")

    # Filtramos nuestro DataFrame con el ramo especificado.
    final = df[df["RAMO"] == nombre]

    final = (
        final.pivot_table(
            index="CICLO", columns="PRESUPUESTO", values="TOTAL", aggfunc="sum"
        )
        / 1000000
    )

    # Ajustamos las cifras por la inflación.
    final["Aprobado_Ajustado"] = final["Aprobado"] * ipc["FACTOR"]
    final["Ejercicio_Ajustado"] = final["Ejercicio"] * ipc["FACTOR"]

    # Creamos los textos para las cifras ajustadas.
    final["Aprobado_Ajustado_Texto"] = final["Aprobado_Ajustado"].apply(abreviar_cifra)
    final["Ejercicio_Ajustado_Texto"] = final["Ejercicio_Ajustado"].apply(
        abreviar_cifra
    )

    # Vamos a crear una tabla con los porcentajes anuales.
    tabla = "<b>Ejercido/Aprobado</b>"

    for k, v in final.iterrows():
        try:
            tabla += f"<br>{k}: {(v['Ejercicio_Ajustado'] / v['Aprobado_Ajustado']) * 100:,.2f}%"
        except:
            # En algunos casos el monto aprobado es 0.
            tabla += f"<br>{k}: ---"

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=final.index,
            y=final["Aprobado_Ajustado"],
            text=final["Aprobado_Ajustado_Texto"],
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=18,
            textposition="outside",
            name="Aprobado",
            marker_color=color1,
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.add_trace(
        go.Bar(
            x=final.index,
            y=final["Ejercicio_Ajustado"],
            text=final["Ejercicio_Ajustado_Texto"],
            textfont_color="#FFFFFF",
            textfont_family="Oswald",
            textfont_size=18,
            textposition="outside",
            name="Ejercido",
            marker_color=color2,
            opacity=1.0,
            marker_line_width=0,
        )
    )

    fig.update_xaxes(
        ticks="outside",
        ticklen=10,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=True,
        gridwidth=0.35,
        mirror=True,
        nticks=15,
    )

    # Vamos a crer el rango para el eje vertical.
    maximo_aprobado = final["Aprobado_Ajustado"].max()
    maximo_ejercido = final["Ejercicio_Ajustado"].max()

    nuevo_maximo = (
        maximo_aprobado if maximo_aprobado >= maximo_ejercido else maximo_ejercido
    )

    fig.update_yaxes(
        range=[0, nuevo_maximo * 1.08],
        title="Millones de pesos a precios constantes de marzo de 2024",
        titlefont_size=20,
        ticks="outside",
        zeroline=False,
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.35,
        showline=True,
        nticks=20,
        mirror=True,
    )

    # Acomodamos la tabla.
    if pos == "left":
        tabla_x = 0.02
        tabla_xanchor = "left"
    elif pos == "right":
        tabla_x = 0.995
        tabla_xanchor = "right"

    fig.update_layout(
        legend_orientation="h",
        legend_itemsizing="constant",
        showlegend=True,
        legend_x=0.5,
        legend_y=1.08,
        legend_xanchor="center",
        legend_yanchor="top",
        width=1280,
        height=720,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=18,
        title_text=f"Evolución del gasto total anual de <b>{titulo}</b> en México",
        title_font_size=24,
        title_x=0.5,
        title_y=0.965,
        margin_t=90,
        margin_l=120,
        margin_r=40,
        margin_b=90,
        plot_bgcolor="#111111",
        paper_bgcolor="#282A3A",
        annotations=[
            dict(
                x=tabla_x,
                y=0.92,
                xref="paper",
                yref="paper",
                xanchor=tabla_xanchor,
                yanchor="top",
                bordercolor="#FFFFFF",
                borderwidth=1.5,
                borderpad=7,
                bgcolor="#111111",
                align="left",
                font_size=12,
                text=tabla,
            ),
            dict(
                x=0.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: SHCP (Cuenta Pública 2013-2022)",
            ),
            dict(
                x=0.5,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año fiscal",
            ),
            dict(
                x=1.01,
                y=-0.14,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image(f"./{archivo}.png")


def comparacion_pib(archivo, tipo, titulo, nota, *elementos):
    """
    Esta función compara el gasto en el ramo/función/etc. esepcificado
    con el PIB del mismo año.

    Parameters
    ==========
    archivo : str
        El nombre que usarmeos para guardar la gráfica.

    tipo : str
        El campo por el cual se filtrarán los datos.

    titulo : str
        La categoría que irá en el título.

    nota : str
        El texto que irá en la anotación.

    elementos : str
        La lista de elementos que se desean filtrar.

    """

    # Cargamos el CSV del PIB nominal.
    pib = pd.read_csv("./assets/PIB.csv", index_col=0)

    # Quitamos los decimales.
    pib *= 1000000

    # Cargamos el dataset de la Cuenta Pública generado por la Secretaría de Economía.
    df = pd.read_csv("./data_se.csv")

    # Filtramos los datos por el tipo de variable y elementos deseados.
    # Estas variables se pueden consultar en la cabecera del dataset.
    df = df[df[tipo].isin(elementos)]

    # Agrupamos por la suma anual y seleccionamos la columna de gasto ejercido.
    df = df.groupby("Year").sum(numeric_only=True)[["Amount Executed"]]

    # Agregamos la columna del PIB nominal.
    df["pib"] = pib

    # Calculamos el porcentaje respecto al PIB.
    df["perc"] = df["Amount Executed"] / df["pib"] * 100

    # Calculamos el cambio orcentual.
    df["change"] = df["perc"].pct_change() * 100

    # Definimos los colores para crecimiento y reduciión.
    df["color"] = df["change"].apply(
        lambda x: "hsl(34, 100%, 20%)" if x < 0 else "hsl(93, 100%, 20%)"
    )

    df["bar_color"] = df["change"].apply(
        lambda x: "hsl(34, 100%, 65%)" if x < 0 else "hsl(93, 100%, 65%)"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["perc"],
            text=df["perc"],
            marker_color=df["bar_color"],
            width=0.05,
            marker_line_width=0,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["perc"],
            mode="markers",
            marker_color=df["color"],
            marker_line_color=df["bar_color"],
            marker_line_width=4,
            marker_size=80,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["perc"] * 0.987,
            text=df["perc"],
            texttemplate="%{text:,.3f}",
            mode="text",
            textposition="middle center",
            textfont_family="Oswald",
            textfont_size=28,
        )
    )

    fig.update_xaxes(
        range=[df.index.min() - 0.6, df.index.max() + 0.6],
        ticks="outside",
        ticklen=10,
        zeroline=False,
        title_standoff=15,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        showgrid=False,
        gridwidth=0.5,
        mirror=True,
        nticks=15,
    )

    fig.update_yaxes(
        range=[0, df["perc"].max() * 1.12],
        title="Porcentaje respecto al PIB anual",
        ticksuffix="%",
        ticks="outside",
        separatethousands=True,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.5,
        showline=True,
        nticks=20,
        mirror=True,
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=720,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=18,
        title_text=f"Evolución del gasto público de México en <b>{titulo}</b> en relación al PIB",
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        title_font_size=24,
        plot_bgcolor="#111111",
        paper_bgcolor="#282A3A",
        annotations=[
            dict(
                x=0.01,
                y=-0.145,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: Hacienda (2013-2022)",
            ),
            dict(
                x=0.5,
                y=-0.145,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Año",
            ),
            dict(
                x=0.5,
                y=0.15,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                bgcolor="#111111",
                align="left",
                bordercolor="#FFFFFF",
                borderwidth=1,
                borderpad=7,
                text=nota,
            ),
            dict(
                x=1.01,
                y=-0.145,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image(f"./{archivo}.png")


def abreviar_cifra(x):
    """
    Esta función abrevia las cifras para que los
    textos no se desborden de las barras verticales.
    """

    if x >= 100000:
        return f"{x/1000:,.0f}k"
    elif x >= 10000:
        return f"{x/1000:,.1f}k"
    else:
        return f"{x:,.0f}"


if __name__ == "__main__":
    # main()
    # main2()

    comparacion_pib(
        7,
        "Function",
        "Ciencia, Tecnología e Innovación",
        "<b>Metodología:</b><br>Se agregó el gasto total clasificado como Ciencia, Tecnología e Innovación,<br>y se ajustó en función del PIB nominal de cada año.",
        "Ciencia, Tecnología e Innovación",
    )

    comparacion_pib(
        8,
        "Department",
        "Salud",
        "<b>Metodología:</b><br>Se agregó el gasto total de los ramos IMSS, ISSSTE y SSA,<br>y se ajustó en función del PIB nominal de cada año.",
        "Instituto Mexicano del Seguro Social",
        "Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado",
        "Salud",
    )
