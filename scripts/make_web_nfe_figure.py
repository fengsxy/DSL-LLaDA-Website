#!/usr/bin/env python3
"""Build the responsive NFE-efficiency figure used by the project page."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"

NFE = np.array([8, 16, 32, 64, 128])
X = np.arange(len(NFE))

SERIES = {
    "DSL-LLaDA-SDE (ours)": {
        "ppl": np.array([12.9, 8.3, 6.1, 5.1, 4.5]),
        "rep": np.array([8.3, 8.7, 6.4, 3.7, 7.5]),
        "length": np.array([174, 174, 185, 187, 154]),
        "color": "#0F4D92",
        "marker": "o",
        "linestyle": "-",
        "linewidth": 3.4,
        "zorder": 4,
    },
    "LLaDA": {
        "ppl": np.array([63.1, 39.1, 20.3, 12.8, 11.5]),
        "rep": np.array([24.8, 21.6, 16.8, 9.5, 0.3]),
        "length": np.array([27, 32, 45, 62, 49]),
        "color": "#5F6662",
        "marker": "s",
        "linestyle": "--",
        "linewidth": 2.7,
        "zorder": 2,
    },
    "LLaDA + EOS + block": {
        "ppl": np.array([6.3, 5.1, 5.3, 7.6, 6.8]),
        "rep": np.array([89.5, 84.5, 71.8, 20.0, 1.5]),
        "length": np.array([116, 143, 163, 182, 179]),
        "color": "#B64342",
        "marker": "D",
        "linestyle": "-.",
        "linewidth": 2.7,
        "zorder": 3,
    },
}


def configure_style(base_font_size: float) -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": base_font_size,
            "axes.linewidth": 1.6,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.labelcolor": "#272C29",
            "axes.titlecolor": "#151816",
            "xtick.color": "#404743",
            "ytick.color": "#404743",
            "legend.frameon": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def draw_series(ax: plt.Axes, metric: str, marker_size: float) -> None:
    for label, style in SERIES.items():
        values = style[metric]
        ax.plot(
            X,
            values,
            color=style["color"],
            label=label,
            linestyle=style["linestyle"],
            linewidth=style["linewidth"],
            zorder=style["zorder"],
        )

        if metric == "ppl" and label == "LLaDA + EOS + block":
            unreliable = np.array([True, True, True, False, False])
            ax.scatter(
                X[unreliable],
                values[unreliable],
                s=marker_size**2,
                marker=style["marker"],
                facecolor="white",
                edgecolor=style["color"],
                linewidth=2.2,
                zorder=style["zorder"] + 1,
            )
            ax.scatter(
                X[~unreliable],
                values[~unreliable],
                s=marker_size**2,
                marker=style["marker"],
                facecolor=style["color"],
                edgecolor="white",
                linewidth=0.9,
                zorder=style["zorder"] + 1,
            )
        else:
            ax.scatter(
                X,
                values,
                s=marker_size**2,
                marker=style["marker"],
                facecolor=style["color"],
                edgecolor="white",
                linewidth=0.9,
                zorder=style["zorder"] + 1,
            )


def build_figure(output: Path, *, mobile: bool) -> None:
    if mobile:
        figsize = (7.2, 13.0)
        base_font_size = 14.5
        legend_columns = 1
        top = 0.82
        left = 0.22
        hspace = 0.42
        marker_size = 7.4
    else:
        figsize = (12.0, 11.4)
        base_font_size = 16.0
        legend_columns = 3
        top = 0.90
        left = 0.13
        hspace = 0.36
        marker_size = 8.6

    configure_style(base_font_size)
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)
    fig.subplots_adjust(
        left=left,
        right=0.975,
        bottom=0.075,
        top=top,
        hspace=hspace,
    )

    metrics = ("ppl", "rep", "length")
    panel_titles = (
        "A   FLUENCY (LOG SCALE)",
        "B   REPETITION",
        "C   OUTPUT LENGTH",
    )
    ylabels = (
        "Generation perplexity ↓",
        "Repetition rate (%) ↓",
        "Average output (words) ↑",
    )

    for ax, metric, title, ylabel in zip(axes, metrics, panel_titles, ylabels):
        ax.axvspan(-0.38, 1.38, color="#EDF3F8", zorder=0)
        ax.grid(axis="y", color="#DDE2DF", linewidth=0.9, alpha=0.9)
        ax.set_axisbelow(True)
        ax.set_xlim(-0.42, len(NFE) - 0.58)
        ax.set_ylabel(ylabel, labelpad=12, fontweight="semibold")
        ax.set_title(title, loc="left", pad=10, fontsize=base_font_size + 1.5)
        ax.xaxis.set_major_locator(FixedLocator(X))
        ax.set_xticklabels([str(value) for value in NFE])
        ax.tick_params(axis="both", width=1.3, length=5)
        draw_series(ax, metric, marker_size)

    axes[0].set_yscale("log")
    axes[0].set_ylim(3.5, 78)
    axes[0].yaxis.set_major_locator(FixedLocator([5, 10, 20, 40, 60]))
    axes[0].yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    axes[1].axhspan(0, 10, color="#E7F3ED", zorder=0)
    axes[1].axhline(10, color="#5C8C78", linewidth=1.2, linestyle=":", zorder=1)
    axes[1].text(
        0.985,
        0.13,
        "10% threshold",
        transform=axes[1].transAxes,
        color="#47715F",
        fontsize=base_font_size - 3.5,
        ha="right",
        va="bottom",
    )
    axes[1].set_ylim(-2, 100)
    axes[1].yaxis.set_major_locator(FixedLocator([0, 20, 40, 60, 80, 100]))

    axes[2].set_ylim(0, 210)
    axes[2].yaxis.set_major_locator(FixedLocator([0, 50, 100, 150, 200]))
    axes[2].set_xlabel(
        "NFE (forward evaluations)",
        labelpad=10,
        fontweight="semibold",
    )

    handles, labels = axes[0].get_legend_handles_labels()
    legend = fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.985),
        ncol=legend_columns,
        columnspacing=2.2,
        handlelength=3.0,
        handletextpad=0.7,
        fontsize=base_font_size,
    )
    for handle, style in zip(legend.legend_handles, SERIES.values()):
        handle.set_marker(style["marker"])
        handle.set_markersize(marker_size)
        handle.set_markerfacecolor(style["color"])
        handle.set_markeredgecolor("white")

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300)
    plt.close(fig)


def main() -> None:
    build_figure(ASSET_DIR / "nfe_efficiency_web.png", mobile=False)
    build_figure(ASSET_DIR / "nfe_efficiency_web_mobile.png", mobile=True)


if __name__ == "__main__":
    main()
