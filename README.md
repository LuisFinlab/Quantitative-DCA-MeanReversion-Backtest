# Quantitative-DCA-MeanReversion-Backtest
Quantitative mean-reversion trading strategy backtest using Backtrader with dynamic DCA position sizing.
# Quantitative DCA & Bollinger Mean Reversion Strategy

## 📌 Overview
An algorithmic trading strategy combining **Bollinger Bands Mean-Reversion** with a dynamic **Dollar-Cost Averaging (DCA)** execution framework built in Python using `Backtrader`.

## 📈 Strategy Logic & Risk Management
- **Initial Entry (25% Capital Allocation):** Triggered when price penetrates and re-enters the lower Bollinger Band with RSI(14) < 50.
- **Scaled Re-entries (DCA):** Up to 4 consecutive entries (25% capital block each) enforced with a minimum 10-day waiting period and lower acquisition prices.
- **Exit Strategy:** Full liquidation only when the position is profitable AND price touches the upper band or RSI >= 60.

## 🛠️ Tech Stack
- Python 3.10+
- Backtrader Framework
- yFinance API & Pandas
