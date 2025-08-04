import h5py
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os

sns.set_theme(style="whitegrid")

waveform_files = {
    "GW170817": {
        "teob": "/home/kkacanja/ecc_pe/gw170817/teob/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw170817/teobHM/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw170817/seob/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw170817/seobHM/posteriors.hdf"
    },
    "GW190425": {
        "teob": "/home/kkacanja/ecc_pe/gw190425/teob/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw190425/teobHM/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw190425/seob/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw190425/seobHM/posteriors.hdf"
    },
    "GW190814": {
        "teob": "/home/kkacanja/ecc_pe/gw190814/teob/workflow/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw190814/seob/workflow/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw190814/teobHM/workflow/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw190814/seobHM/workflow/posteriors.hdf"
    },
    "GW200105": {
        "teob": "/home/kkacanja/ecc_pe/gw200105/teob/workflow/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw200105/seob/workflow/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw200105/teobHM/workflow/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw200105/seobHM/workflow/posteriors.hdf"
    },
    "GW200115": {
        "teob": "/home/kkacanja/ecc_pe/gw200115/teob/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw200115/teobHM/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw200115/seob/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw200115/seobHM/posteriors.hdf"
    },
    "GW230529": {
        "teob": "/home/kkacanja/ecc_pe/gw230529/teob/posteriors.hdf",
        "seob": "/home/kkacanja/ecc_pe/gw230529/seob/posteriors.hdf",
        "teobHM": "/home/kkacanja/ecc_pe/gw230529/teobHM/posteriors.hdf",
        "seobHM": "/home/kkacanja/ecc_pe/gw230529/seobHM/posteriors.hdf"
    },
}

output_dir = "/home/kkacanja/public_html/ecc_pe/plots/"
os.makedirs(output_dir, exist_ok=True)

model_colors = {
    "teob": "orange",
    "seob": "#024CAA",
    "teobHM": "red",
    "seobHM": "green"
}

def kde_with_reflection(data, bw_smoothing=0.01, grid_points=1000):
    reflected_data = np.concatenate([-data[data < 0.02], data])
    kde = gaussian_kde(reflected_data, bw_method=bw_smoothing)
    x_vals = np.linspace(0, np.max(data) * 1.1 if len(data) > 0 else 0.1, grid_points)
    y_vals = kde(x_vals)
    y_vals *= 2
    return x_vals, y_vals

def plot_kde_with_intervals(ax, data, model_name, color, kde_bandwidth, credible_interval_type):
    median = np.percentile(data, 50)
    credible_interval_text = ""

    if credible_interval_type == 'upper_bound':
        e_90_percentile = np.percentile(data, 90)
        credible_interval_text = f'$e < {e_90_percentile:.3f}$ (90%)'
        x_vals, y_vals = kde_with_reflection(data, bw_smoothing=kde_bandwidth)
        ax.plot(x_vals, y_vals, label=f"{model_name}: {credible_interval_text}", color=color, linewidth=2)
        ax.axvline(e_90_percentile, color=color, linestyle="--", alpha=0.7, linewidth=1.2)

    elif credible_interval_type == 'symmetric':
        e_5 = np.percentile(data, 5)
        e_95 = np.percentile(data, 95)
        lower_error = median - e_5
        upper_error = e_95 - median
        credible_interval_text = f'$e = {median:.3f}^{{+{upper_error:.3f}}}_{{-{lower_error:.3f}}}$'
        x_vals, y_vals = kde_with_reflection(data, bw_smoothing=kde_bandwidth)
        ax.plot(x_vals, y_vals, label=f"{model_name}: {credible_interval_text}", color=color, linewidth=2)
        ax.axvline(median, color=color, linestyle="-", alpha=0.7, linewidth=1.5)
        ax.axvline(e_5, color=color, linestyle="--", alpha=0.7, linewidth=1.2)
        ax.axvline(e_95, color=color, linestyle="--", alpha=0.7, linewidth=1.2)
    else:
        print(f"Warning: Unknown credible_interval_type '{credible_interval_type}'")
        x_vals, y_vals = kde_with_reflection(data, bw_smoothing=kde_bandwidth)
        ax.plot(x_vals, y_vals, label=f"{model_name}", color=color, linewidth=2)

fig, axs = plt.subplots(2, 3, figsize=(18, 10))
axs = axs.flatten()

for idx, (source_name, models) in enumerate(waveform_files.items()):
    ax = axs[idx]

    if source_name == "GW200105":
        kde_bw = 0.14
        interval_type = 'symmetric'
    else:
        kde_bw = 0.3
        interval_type = 'upper_bound'

    for model_name, file_path in models.items():
        if not os.path.exists(file_path):
            print(f"Warning: Missing file {file_path}. Skipping.")
            continue

        try:
            with h5py.File(file_path, "r") as f:
                if "samples" in f and "eccentricity" in f["samples"]:
                    data = f["samples/eccentricity"][:]
                    plot_kde_with_intervals(ax, data, model_name.upper(), model_colors[model_name], kde_bw, interval_type)
                else:
                    print(f"Warning: Missing 'samples/eccentricity' in {file_path}. Skipping.")
        except Exception as e:
            print(f"Error processing {file_path}: {e}. Skipping.")
            continue

    ax.set_title(f"{source_name}", fontsize=16)
    ax.set_xlabel(r"$e$", fontsize=16)
    ax.set_ylabel("Density", fontsize=16)
    ax.set_xlim(left=0)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.legend(fontsize=12)

plt.rcParams['font.family'] = 'Times New Roman'
plt.tight_layout()
plot_filename = os.path.join(output_dir, "eccentricity_comparison.png")
plt.savefig(plot_filename, dpi=300)
plt.close(fig)

print(f"\nPlot saved to {plot_filename}")
