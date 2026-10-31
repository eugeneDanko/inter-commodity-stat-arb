"""Build a compact portfolio chart from the saved confirmed result table."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent


def main() -> None:
    frame = pd.read_csv(ROOT / "portfolio_summary.csv")
    print(frame.to_string(index=False))

    label_col = frame.columns[0]
    numeric = frame.select_dtypes("number")
    if numeric.shape[1] < 3:
        raise ValueError("portfolio_summary.csv does not contain the expected numeric metrics")

    labels = frame[label_col].astype(str).str.replace("_", " ").str.title()
    return_col = next((c for c in numeric if "return" in c.lower()), numeric.columns[0])
    sharpe_col = next((c for c in numeric if "sharpe" in c.lower()), numeric.columns[-2])
    drawdown_col = next(
        (c for c in numeric if "drawdown" in c.lower() or "maxdd" in c.lower()),
        numeric.columns[-1],
    )

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, column, title in zip(
        axes,
        [return_col, sharpe_col, drawdown_col],
        ["Annualized return", "Sharpe ratio", "Maximum drawdown"],
    ):
        values = frame[column]
        colors = ["#3a7d5d" if value >= 0 else "#b24b4b" for value in values]
        ax.barh(labels, values, color=colors)
        ax.axvline(0, color="#333333", linewidth=0.8)
        ax.set_title(title)
        ax.set_xlabel(column)
    fig.suptitle("Confirmed inter-commodity statistical-arbitrage results", fontsize=13)
    fig.tight_layout()
    fig.savefig(ROOT / "stat_arb_summary.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
