# Demand / supply levels

Enter a ticker, see the daily (1Y) and weekly (2Y) support/resistance chart.
`spy_qqq_levels.py` is the original script, unchanged apart from removing the AutoTasks report block and downloading dividend-adjusted bars (Adj Close / Close, as TradingView with ADJ on); `app.py` is the page. Tests: `pytest tests`.

Run locally: `pip install -r requirements.txt && streamlit run app.py`
Deploy: share.streamlit.io -> New app -> pick this repo, branch main, file `app.py`.
