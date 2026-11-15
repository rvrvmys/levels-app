"""levels-app draws its SMAs, zones and chart from dividend-adjusted bars, never raw (as traded) ones."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import spy_qqq_levels as lv  # noqa: E402


def _bars():
    idx = pd.bdate_range("2026-01-05", periods=3, tz="America/New_York")
    c = pd.Series([100.0, 102.0, 104.0], index=idx)
    return pd.DataFrame({"Open": c, "High": c + 1, "Low": c - 1, "Close": c,
                         "Adj Close": [98.0, 100.0, 104.0], "Volume": 100.0}, index=idx)


def test_fetch_data_returns_adjusted_bars(monkeypatch):
    import yfinance

    class FakeTicker:
        def __init__(self, t):
            pass

        def history(self, **kw):
            assert kw.get("auto_adjust") is False      # Adj Close is needed to scale the bars here
            return _bars()

    monkeypatch.setattr(yfinance, "Ticker", FakeTicker)
    df = lv.fetch_data("SPY", "2y", "1d")
    assert df["Close"].tolist() == [98.0, 100.0, 104.0]
    assert df["High"].iloc[0] == pytest.approx(101 * 0.98)
    assert df["Close"].iloc[-1] == 104.0 and df["Volume"].tolist() == [100.0] * 3
    assert df.index.tz is None


def test_adjust_is_idempotent_and_skips_bars_without_adj_close():
    once = lv.adjust(_bars())
    assert lv.adjust(once).equals(once)
    plain = _bars().drop(columns="Adj Close")
    assert lv.adjust(plain).equals(plain)
