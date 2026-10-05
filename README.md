# Quantitative DCA & Bollinger Mean Reversion Strategy

## 📌 Overview
An algorithmic trading strategy combining **Bollinger Bands Mean-Reversion** with a dynamic **Dollar-Cost Averaging (DCA)** execution framework built in Python using `Backtrader`.

The model incorporates strict liquidity validation (`broker.getcash()`), exact candlestick price action mechanics (evaluating low-wick band penetrations), and a multi-entry risk management engine.

---

## 📈 Strategy Logic & Risk Management
- **Initial Entry (25% Capital Allocation):** Triggered when the asset's low price (`Low[-1]`) penetrates the lower Bollinger Band and subsequently re-enters the band with `RSI(14) < 50`.
- **Scaled Re-entries (DCA):** Up to 4 consecutive entries (25% capital block each) enforced with a minimum 10-day waiting period and lower acquisition prices. Liquidity is validated before order execution.
- **Exit Strategy:** Full liquidation only when the total position is profitable AND price touches the upper band or `RSI >= 60`.

---

## 📊 Quantitative Metrics & Risk Analysis
The backtesting engine integrates automated performance analyzers (`bt.analyzers`):
- **Risk-Adjusted Return:** Sharpe Ratio calculation with a configurable risk-free rate.
- **Drawdown Analysis:** Maximum Drawdown (Max DD) tracking throughout the simulation period.
- **Trade Analytics:** Win rate, trade duration, and execution history validation via `TradeAnalyzer`.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Backtrader** (Backtesting Framework)
- **yFinance API & Pandas** (Data Ingestion & Cleaning)
- **Matplotlib** (Candlestick Visualization)

---

## 🚀 Getting Started
```bash
# 1. Clone Repository
git clone [https://github.com/LuisFinlab/Quantitative-DCA-MeanReversion-Backtest.git](https://github.com/LuisFinlab/Quantitative-DCA-MeanReversion-Backtest.git)

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Run Historical Backtest
python main.py
