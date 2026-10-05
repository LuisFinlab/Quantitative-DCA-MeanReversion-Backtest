import datetime
import os
import backtrader as bt
from strategies.BollingerDCA import BollingerMeanReversion

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BollingerMeanReversion)

    # 🟢 CORRECCIÓN DE MAPEO DE COLUMNAS CSV (yFinance Standard Output)
    # yFinance exporta: Date(0), Open(1), High(2), Low(3), Close(4), Adj Close(5), Volume(6)
    data_path = 'data/MSFT_historical_data.csv'

    if os.path.exists(data_path):
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
            volume=6,
            openinterest=-1
        )
        cerebro.adddata(data)

    # Configuración de Broker
    capital_inicial = 10000.0
    cerebro.broker.setcash(capital_inicial)
    cerebro.broker.setcommission(commission=0.001)  # 0.1% comisión

    # 📊 MEJORA: Incorporación de Analizadores Cuantitativos
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.04)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    print(f'--- INICIO DE BACKTEST ---')
    print(f'Capital Inicial: ${capital_inicial:,.2f}')

    results = cerebro.run()
    strat = results[0]

    capital_final = cerebro.broker.getvalue()
    retorno_pct = ((capital_final - capital_inicial) / capital_inicial) * 100

    # Extraer métricas
    sharpe = strat.analyzers.sharpe.get_analysis().get('sharperatio', None)
    max_dd = strat.analyzers.drawdown.get_analysis().get('max', {}).get('drawdown', 0.0)
    trades = strat.analyzers.trades.get_analysis()
    total_trades = trades.get('total', {}).get('closed', 0)

    print(f'\n--- RESULTADOS METRICOS ---')
    print(f'Capital Final:   ${capital_final:,.2f} ({retorno_pct:+.2f}%)')
    print(f'Sharpe Ratio:    {sharpe:.2f}' if sharpe else 'Sharpe Ratio:    N/A')
    print(f'Max Drawdown:    {max_dd:.2f}%')
    print(f'Trades Cerrados: {total_trades}')

    # Graficar
    cerebro.plot(style='candlestick')