"""

utils.py — Módulo central de rutas y funciones compartidas


Uso en cualquier notebook del curso:

    import sys
    sys.path.append('/content/drive/MyDrive/CUGDL/Fundamentos_de_Ingenieria_de_Datos/Utilidades')
    from utils import PROYECTO_BASE . .. (otras rutas y funciones)

    
Funciones disponibles:

    Inspección   : inspeccionar_dataset(), listar_tablas()

s
    Este archivo se actualiza en la medida en que nuevos notebooks necesitan nuevas rutas o funciones compartidas

"""

# ── Librerías ─────────────────────────────────────────────────────────────────

import os
import json
import sqlite3
import pandas as pd
from datetime import datetime


# ==============================================================================

# RUTAS DEL PROYECTO

PROYECTO_BASE = '/Users/artdeco/Documents/CUGDL/Ingenieria_de_datos'

#/Users/artdeco/Documents/CUGDL/Ingenieria_de_datos



# ── Capa de ingesta ────────────────────────────────────────────────

DATASETS_RAW_PATH = f'{PROYECTO_BASE}/Ingesta_de_Datos/Datasets_raw'
DB_PATH           = f'{PROYECTO_BASE}/Ingesta_de_Datos/Base_de_datos/base_datos.db'


# ==============================================================================
# FUNCIONES DE INSPECCIÓN


def inspeccionar_dataset(df, nombre='Dataset'):

    """

    Muestra un perfil básico de un DataFrame:
    dimensiones, tipos de datos, valores nulos y primeras filas.

    Parámetros:

        df     : DataFrame a inspeccionar
        nombre : etiqueta descriptiva para el encabezado

    """


    print(f'\n{"=" * 55}')
    print(f'  DATASET: {nombre}')
    print(f'{"=" * 55}')
    print(f'  Filas    : {df.shape[0]:,}')
    print(f'  Columnas : {df.shape[1]}')
    print(f'\n  Tipos de datos y valores nulos:')

    for col, dtype in df.dtypes.items():
        nulos = df[col].isna().sum()
        pct = nulos / len(df) * 100
        print(f'    {col:<28} {str(dtype):<12} nulos: {nulos} ({pct:.1f}%)')

    print(f'\n  Primeras 3 filas:')
    try:
        from IPython.display import display
        display(df.head(3))
    except ImportError:
        print(df.head(3).to_string())
    print()




def listar_tablas(db_path=None):

    """
    Lista todas las tablas del archivo .db clasificadas por capa
    (raw_, extracted_, transformed_, serving_).

    Parámetros:
        db_path : ruta al archivo .db (usa DB_PATH por defecto)

    Retorna:
        Lista con los nombres de las tablas encontradas
    """

    if db_path is None:
        db_path = DB_PATH

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [row[0] for row in cursor.fetchall()]

    print(f'\n  Tablas en: {os.path.basename(db_path)}\n')
    print(f'  {"TABLA":<35} {"CAPA":<15} {"FILAS":>8} {"COLS":>6}')
    print(f'  {"-"*35} {"-"*15} {"-"*8} {"-"*6}')

    for tabla in tablas:
        df_t = pd.read_sql_query(f'SELECT * FROM "{tabla}"', conn)
        capa = tabla.split('_')[0] + '_' if '_' in tabla else 'otra'
        print(f'  {tabla:<35} {capa:<15} {df_t.shape[0]:>8,} {df_t.shape[1]:>6}')

    conn.close()
    return tablas


