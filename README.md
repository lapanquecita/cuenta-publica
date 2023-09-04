# Cuenta Pública

En este repositorio se encuentran scripts para poder analizar los archivos de Cuenta Pública de México de los años 2013-2022.

La Secretaría de Hacienda y Crédito Público (SHCP) tiene a disposición estos documentos en distintos formatos: .pdf, .doc, .xls y .csv, sin embargo no están estructurados de una forma fácil o intuitiva de analizar. El objetivo de este repositorio es proveer esta misma información de una manera eficiente.

Los archivos `.xls` son obtenidos del siguiente sitio web: https://www.cuentapublica.hacienda.gob.mx/

Para extraer la información se sigue un proceso el cual se detalla a continuación.

## Extracción de la infomación

La SHCP, en su portal de Cuenta Pública provee información desde el año 1996, sin embargo solo a partir del año 2013 esta información se encuentra desglosada de manera detallada.

El primer paso es descargar todos los archivos `.xls` y renombrarlos a su ciclo (año) correspondiente. Estos archivos se encuentran en la carpeta `xls`.

El siguiente paso es extraer la información de dichos archivos, el desafío más grande es su estructura jerárquica. El script `converter.py` se encarga de extraer fila por fila y recordar cuales son las categorías padre de cada una.

Una vez que se extrae la información de cada archivo `.xls` se guarda en un nuevo archivo `.csv`. Estos archivos después son unidos en uno solo llamado `data.csv`.

Es importante mencionar que al archivo `data.csv` se le aplican varios filtros para remover datos duplicados e innecesarios que causan inconsistencias al hacer operaciones vectoriales (como sumar totales).

## Validación de la información

El principal objetivo de este proyecto es poder conocer de manera rápida y sencilla los totales de cada ente, ramo y programa. Para verificar que estos valores sean los correctos se cruzaron con los resultados de los reportes en `.pdf` que se encuentran en el mismo sitio web que los demás archivos.

Los siguientes 4 valores son obtenidos del archivo `.pdf` del año 2022.

* Aprobado 2022 - Poder Legislativo: 15,012.6
* Aprobado 2022 - Poder Judicial: 73,723.0
* Aprobado 2022 - Órganos Autónomos: 56,685.4
* Aprobado 2022 - Ramos Administrativos: 1,514,103.4

Para obtener estas cifras utilizaremos el siguiente código:

```python
df = pd.read_csv("./data.csv")
df = df[df["CICLO"] == 2022]

df = df.pivot_table(index="ENTE", columns="PRESUPUESTO", values="TOTAL", aggfunc="sum")
df = (df / 1000000).round(decimals=1)

print(df)
```

Lo cual nos devolverá la siguiente tabla:

| ENTE                  |        Aprobado |       Devengado |       Ejercicio |      Modificado |
|:----------------------|----------------:|----------------:|----------------:|----------------:|
| Poder Judicial        | 73723           | 74141.7         | 74141.7         | 74181.1         |
| Poder Legislativo     | 15012.6         | 15620.4         | 15620.4         | 15620.4         |
| Ramos Administrativos |     1.5141e+06  |     1.87359e+06 |     1.87359e+06 |     1.87359e+06 |
| Ramos Generales       |     3.70427e+06 |     3.77473e+06 |     3.77473e+06 |     3.77473e+06 |
| Órganos Autónomos     | 56685.4         | 56387.9         | 56387.9         | 56666.4         |

Efectivamente, los 4 valores coinciden sin necesidad de hacer transformaciones adicionales.

El único detalle pendiente es encontrar la combianación de ramos para el total de `Ramos Generales`.

## Notas

En el archivo `data.csv` hay algunas columnas con sufijo, este puede ser `GC` (Gasto Corriente) o `GI` (Gasto de Inversión).

Algunos ramos fueron renombrados a su nombre actual, como es el caso de Desarrollo Social el cual ahora se llama Bienestar.

LAs cifras no estána ajustadas con la inflación.

Existe otro conjunto de bases de datos de Cuenta Pública (https://www.transparenciapresupuestaria.gob.mx/Datos-Abiertos), sin embargo, encontré varias inconsistencias al calcular los totales. También había un par de archivos con filas mucho más largas que las demás. Por lo tanto opté no usarlos para este repositorio.

Los archivos antes mencionados están mucho más detallados, al incluir información por Entidad Federativa (en algunos casos). Los recomiendo consultar si se desea indagar más a fondo.
