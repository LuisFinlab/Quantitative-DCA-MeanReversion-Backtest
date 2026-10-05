import datetime
import os
import sys
import pandas as pd
import backtrader as bt
import yfinance as yf
from BollingerDCA import BollingerMeanReversion


def obtener_ruta_datos():
    """
    Gestiona la carga o descarga automática de datos históricos desde Yahoo Finance.
    Genera un archivo CSV estándar limpio compatible con Backtrader.
    """
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        if os.path.exists(ruta):
            print(f"Cargando archivo personalizado: {ruta}")
            return ruta
        else:
            print(f"⚠️ El archivo '{ruta}' no existe. Generando datos por defecto...")

    os.makedirs('data', exist_ok=True)
    ruta_default = 'data/MSFT_historical_data.csv'

    if not os.path.exists(ruta_default):
        print("📥 Descargando datos históricos desde Yahoo Finance...")
        df = yf.download('MSFT', start='2020-01-01', end='2026-12-31')

        # Aplanar MultiIndex de columnas si yfinance entrega encabezados dobles
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Reordenar y formatear columnas exactamente en el orden estándar
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.to_csv(ruta_default)
        print(f"✅ Datos guardados correctamente en {ruta_default}")

    return ruta_default


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BollingerMeanReversion)

    # Cargar datos
    data_path = obtener_ruta_datos()

    # Mapeo estándar de columnas CSV
    data = bt.feeds.GenericCSVData(
        dataname=data_path,
        fromdate=datetime.datetime(2020, 1, 1),
        todate=datetime.datetime(2026, 12, 31),
        nullvalue=0.0,
        dtformat='%Y-%m-%d',
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    cerebro.adddata(data)

    # Configuración de Broker
    capital_inicial = 10000.0
    cerebro.broker.setcash(capital_inicial)
    cerebro.broker.setcommission(commission=0.001)

    # Analizadores Cuantitativos
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.04)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    print('\n--- INICIO DE BACKTEST ---')
    print(f'Capital Inicial: ${capital_inicial:,.2f}')

    results = cerebro.run()
    strat = results[0]

    capital_final = cerebro.broker.getvalue()
    retorno_pct = ((capital_final - capital_inicial) / capital_inicial) * 100

    sharpe = strat.analyzers.sharpe.get_analysis().get('sharperatio', None)
    max_dd = strat.analyzers.drawdown.get_analysis().get('max', {}).get('drawdown', 0.0)
    trades = strat.analyzers.trades.get_analysis()
    total_trades = trades.get('total', {}).get('closed', 0)

    print('\n--- RESULTADOS METRICOS ---')
    print(f'Archivo Evaluado: {data_path}')
    print(f'Capital Final:    ${capital_final:,.2f} ({retorno_pct:+.2f}%)')
    print(f'Sharpe Ratio:     {sharpe:.2f}' if sharpe else 'Sharpe Ratio:     N/A')
    print(f'Max Drawdown:     {max_dd:.2f}%')
    print(f'Trades Cerrados:  {total_trades}')

    # 📊 Renderizar el gráfico interactivo de Matplotlib
    cerebro.plot(style='candlestick', barup='green', bardown='red')
