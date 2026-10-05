import os
import yfinance as yf

#  Elige el ticker que quieras descargar (Ejemplo: KO, GOOGL o SPY) el periodo y la temporalidad de cada Vela
ticker = "MSFT"
periodo_maximo = "max"
temporalidad = "1d"

print(f"Descargando datos para {ticker}...")

data = yf.download(
    tickers=ticker,
    period=periodo_maximo,
    interval=temporalidad,
    multi_level_index=False
)

if data.empty:
    print("❌ Error: No se descargaron datos.")
else:
    # 🟢 SOLUCIÓN AL VALUEERROR: Removemos la zona horaria (-04:00) para dejar la fecha limpia
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)

    if 'Adj Close' not in data.columns and 'Close' in data.columns:
        data['Adj Close'] = data['Close']

    columnas_validas = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    try:
        data = data[columnas_validas]

        modpath = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(modpath, f"{ticker}_historical_data.csv")

        data.to_csv(ruta_csv)

        print(f"✅ ¡Datos guardados sin zona horaria en: {ruta_csv}!")
        print(f"📊 Total de velas descargadas: {len(data)}")

    except KeyError as e:
        print(f"❌ Error de columnas: {e}")
