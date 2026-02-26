import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# 1. DEFINICIÓN DEL UNIVERSO (TU LISTA)
# ==========================================
# Diccionario {Nombre: Ticker_Base}. 
# Nota: He corregido algunos tickers estándar de Yahoo (ej. Ebro -> EBRO) 
# para maximizar la tasa de éxito.

empresas = {
    # --- IBEX 35 ---
    "Acciona": "ANA", "Acciona Energía": "ANE", "Acerinox": "ACX", "ACS": "ACS",
    "Aena": "AENA", "Amadeus": "AMS", "ArcelorMittal": "MTS", "BBVA": "BBVA",
    "Banco Sabadell": "SAB", "Bankinter": "BKT", "CaixaBank": "CABK", "Cellnex": "CLNX",
    "Enagás": "ENG", "Endesa": "ELE", "Ferrovial": "FER", "Fluidra": "FDR",
    "Grifols": "GRF", "IAG": "IAG", "Iberdrola": "IBE", "Inditex": "ITX",
    "Indra": "IDR", "Colonial": "COL", "Logista": "LOG", "Mapfre": "MAP",
    "Merlin": "MRL", "Naturgy": "NTGY", "Puig": "PUIG", "Redeia": "RED", # REE a veces es RED en YF
    "Repsol": "REP", "Rovi": "ROVI", "Sacyr": "SCYR", "Santander": "SAN",
    "Solaria": "SLR", "Telefónica": "TEF", "Unicaja": "UNI",
    
    # --- RESTO MERCADO CONTINUO ---
    "Adolfo Domínguez": "ADZ", "Aedas Homes": "AEDAS", "Airbus": "AIR", 
    "Airtificial": "AI", "Alantra": "ALNT", "Almirall": "ALM", "Amper": "AMP",
    "AmRest": "EAT", "Aperam": "APAM", "Arima": "ARM", "Atresmedia": "A3M",
    "Audax": "ADX", "Azkoyen": "AZK", "Berkeley": "BKY", "Bodegas Riojanas": "RIO",
    "CIE Automotive": "CIE", "CAF": "CAF", "Cash": "CASH", "Clínica Baviera": "CBAV",
    "Cevasa": "CEV", "Coca-Cola EP": "CCEP", "Deoleo": "OLE", "Dia": "DIA",
    "Duro Felguera": "MDF", "Ebro Foods": "EBRO", "EDreams": "EDR", "Elecnor": "ENO",
    "ENCE": "ENC", "Ercros": "ERC", "Ezentis": "EZE", "Faes Farma": "FAE",
    "FCC": "FCC", "GAM": "GALQ", "Gestamp": "GEST", "Dominion": "DOM",
    "Grenergy": "GRE", "GCO": "GCO", "Iberpapel": "IBG", "Inm. del Sur": "ISUR",
    "Izertis": "IZER", "Lingotes": "LGT", "Meliá": "MEL", "Metrovacesa": "MVC",
    "Miquel Costa": "MCM", "Montebalito": "MBT", "Naturhouse": "NTH", 
    "Neinor": "HOME", "Nextil": "NXT", "NH Hotel": "NHH", "Nicolás Correa": "NEA",
    "Nueva Pescanova": "PVA", "Nyesa": "NYE", "OHLA": "OHLA", "Oryzon": "ORY",
    "PharmaMar": "PHM", "Prim": "PRM", "Prisa": "PRS", "Prosegur": "PSG",
    "Realia": "RLIA", "Reig Jofre": "RJF", "Renta 4": "R4", "Renta Corp": "REN",
    "Reno de Medici": "RDM", "San Jose": "GSJ", "Soltec": "SOL", "Squirrel": "SQRL",
    "Talgo": "TLGO", "Técnicas Reunidas": "TRE", "Tubacex": "TUB", 
    "Tubos Reunidos": "TRG", "Urbas": "UBS", "Vidrala": "VID", "Viscofan": "VIS",
    "Vocento": "VOC"
}

# ==========================================
# 2. CONFIGURACIÓN DE DESCARGA
# ==========================================
START_DATE = "2004-01-01"
END_DATE = datetime.today().strftime('%Y-%m-%d')

print(f"Iniciando descarga ROBUSTA para {len(empresas)} empresas...")

dfs = []
errores = []

for nombre, ticker_base in empresas.items():
    ticker_yf = f"{ticker_base}.MC"
    
    try:
        # CORRECCIÓN 1: auto_adjust=False fuerza a que traiga 'Adj Close' explícitamente
        df = yf.download(ticker_yf, start=START_DATE, end=END_DATE, progress=False, auto_adjust=False)
        
        if df.empty:
            errores.append(f"{nombre}: Sin datos.")
            continue
            
        # CORRECCIÓN 2: Aplanar MultiIndex (Causa principal del error)
        # Si las columnas son tuplas tipo ('Adj Close', 'SAN.MC'), nos quedamos solo con el nombre
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Reset index para que 'Date' sea columna
        df = df.reset_index()
        
        # Todo a minúsculas y quitar espacios extra
        df.columns = [c.lower().strip() for c in df.columns]
        
        # CORRECCIÓN 3: Búsqueda flexible de la columna de cierre
        # Buscamos 'adj close', si no está, usamos 'close'
        col_precio = None
        if 'adj close' in df.columns:
            col_precio = 'adj close'
        elif 'close' in df.columns:
            col_precio = 'close'
        elif 'adjclose' in df.columns: # A veces yfinance lo junta
            col_precio = 'adjclose'
            
        if col_precio is None:
            errores.append(f"{nombre}: No se encontró columna de precio (Columnas: {list(df.columns)})")
            continue

        # Renombrar la columna encontrada a 'adjusted_close'
        df = df.rename(columns={col_precio: 'adjusted_close', 'date': 'ds'})
        
        # Verificar que tenemos la columna fecha 'ds'
        if 'ds' not in df.columns:
             # A veces la fecha sigue en el índice tras reset_index si no se llama 'Date'
             # Forzamos que la primera columna sea 'ds' si es datetime
             if pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
                 df.rename(columns={df.columns[0]: 'ds'}, inplace=True)

        # 1. Identificador único
        df['unique_id'] = ticker_base
        
        # 2. Variable Objetivo
        # Ahora es seguro porque 'adjusted_close' existe sí o sí
        df['y'] = np.log(df['adjusted_close'] / df['adjusted_close'].shift(1))
        
        # 3. Features
        df['vol_log'] = np.log(df['volume'] + 1)
        
        # Seleccionar columnas finales
        cols_deseadas = ['unique_id', 'ds', 'open', 'high', 'low', 'volume', 'adjusted_close', 'vol_log', 'y']
        # Intersección para evitar error si falta alguna (ej. open/high)
        cols_finales = [c for c in cols_deseadas if c in df.columns]
        df = df[cols_finales]
        
        df = df.dropna(subset=['y'])
        
        dfs.append(df)
        print(f"✅ {nombre}: OK.")

    except Exception as e:
        errores.append(f"Error crítico en {nombre}: {str(e)}")

# ==========================================
# 3. CONSOLIDACIÓN Y GUARDADO
# ==========================================
if dfs:
    full_df = pd.concat(dfs)
    
    # Ordenar
    full_df = full_df.sort_values(by=['unique_id', 'ds'])
    
    # Guardar
    archivo_salida = "dataset_mercado_continuo_20y.csv"
    full_df.to_csv(archivo_salida, index=False)
    
    print(f"\nProceso finalizado.")
    print(f"Dataset guardado en: {archivo_salida}")
    print(f"Dimensiones: {full_df.shape}")
    print(f"Total empresas procesadas con éxito: {len(full_df['unique_id'].unique())}")
else:
    print("No se han podido descargar datos.")

if errores:
    print("\nReporte de incidencias:")
    for err in errores:
        print(err)