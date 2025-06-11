import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#202124'
plt.rcParams['axes.facecolor'] = '#232629'
plt.rcParams['axes.edgecolor'] = '#444'
plt.rcParams['axes.labelcolor'] = '#DDDDDD'
plt.rcParams['xtick.color'] = '#BBBBBB'
plt.rcParams['ytick.color'] = '#BBBBBB'
plt.rcParams['legend.facecolor'] = '#353535'

def human_unit_and_scale(val):
    """Choose human-friendly time unit and scale factor based on a value in nanoseconds."""
    if val >= 1_000_000_000:
        return "s", 1e-9
    elif val >= 1_000_000:
        return "ms", 1e-6
    elif val >= 1_000:
        return "μs", 1e-3
    else:
        return "ns", 1


def parse_csv(filename):
    rows = []
    with open(filename, newline='') as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            row = [i.strip() for i in line.split(",", 1)]
            if row[0] == "ACCEL_CYCLES":
                rows.append({"ns": row[1]})
    df = pd.DataFrame(rows)
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Compare touchpad runtime logs (nanoseconds input).")
    parser.add_argument("csv_files", nargs='+',
                        help="One or two CSV files to compare")
    parser.add_argument("--max-samples", type=int, default=None,
                        help="Cap the number of samples plotted from each file")
    args = parser.parse_args()

    if not (1 <= len(args.csv_files) <= 2):
        parser.error("You must provide one or two CSV files.")

    styles = ["-o", "-s"]
    colors = ["#A6CEE3", "#FDBF6F", "#B2DF8A", "#BC80BD"]

    plt.figure(figsize=(13, 7))

    for idx, csv_file in enumerate(args.csv_files):
        label = os.path.basename(csv_file)
        df = parse_csv(csv_file)
        df["ns"] = pd.to_numeric(df["ns"], errors="coerce")
        df = df.dropna()
        if args.max_samples is not None:
            df = df.iloc[:args.max_samples]

        min_ns = df["ns"].min()
        max_ns = df["ns"].max()
        avg_ns = df["ns"].mean()

        base_unit, scale = human_unit_and_scale(avg_ns)
        df["pretty"] = df["ns"] * scale
        min_display = min_ns * scale
        max_display = max_ns * scale
        avg_display = avg_ns * scale

        plt.plot(df["pretty"].values,
                 styles[idx % len(styles)],
                 color=colors[idx % len(colors)],
                 alpha=0.7,
                 linewidth=0.5,
                 label=f"{label}",
                 markersize=2)

        plt.axhline(avg_display, color=colors[idx % len(colors)], linestyle="--", alpha=0.8,
                    label=f"{label} mean: {avg_display:.2f}{base_unit}")
        plt.axhline(min_display, color=colors[idx % len(colors)], linestyle=":", alpha=0.7,
                    label=f"{label} min: {min_display:.2f}{base_unit}")
        plt.axhline(max_display, color=colors[idx % len(colors)], linestyle=":", alpha=0.7,
                    label=f"{label} max: {max_display:.2f}{base_unit}")

        # Annotate values
        x_label_pos = len(df) + 100
        plt.text(x_label_pos, avg_display, f"mean: {avg_display:.2f}{base_unit}",
                 color=colors[idx % len(colors)], va='bottom', ha='left', fontsize=9, style='italic')
        plt.text(x_label_pos, min_display-5, f"min: {min_display:.2f}{base_unit}",
                 color=colors[idx % len(colors)], va='bottom', ha='left', fontsize=9)
        plt.text(x_label_pos, max_display, f"max: {max_display:.2f}{base_unit}",
                 color=colors[idx % len(colors)], va='bottom', ha='left', fontsize=9)

        print(f"{label}: min={min_display:.2f} {base_unit}, max={
              max_display:.2f} {base_unit}, mean={avg_display:.2f} {base_unit}")

        plt.ylabel(f"Time ({base_unit})")

    plt.title("Acceleration Function Runtime Comparison")
    plt.xlabel("Sample")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
