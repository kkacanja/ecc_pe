import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# File paths
paths = {
    "teob_log": "/home/kkacanja/ecc_pe/gw200105/teob/workflowlog/posteriors.hdf",
    "teob_uniform": "/home/kkacanja/ecc_pe/gw200105/teob/workflow/posteriors.hdf",
    "seob_uniform": "/home/kkacanja/ecc_pe/gw200105/seob/workflow/posteriors.hdf",
    "seob_log": "/home/kkacanja/ecc_pe/gw200105/seob/workflowlog/posteriors.hdf"
}

# Colors
colors = {
    "teob_log": "#FFD23E",
    "teob_uniform": "orange",
    "seob_uniform": "#0A57BB",
    "seob_log": "#39C4C9"
}

# Labels
labels = {
    "teob_log": "TEOB (LOG (2,2) MODE) $e_{{\\min}} = 10^{{-4}}$",
    "teob_uniform": "TEOB (UNIFORM (2,2) MODE)",
    "seob_uniform": "SEOBNRv5EHM (UNIFORM (2,2) MODE)",
    "seob_log": "SEOBNRv5EHM (LOG (2,2) MODE) $e_{{\\min}} = 10^{{-4}}$"
}

def get_percentile(data, percentile):
    return np.percentile(data, percentile)

# Load and process each dataset
results = {}
for key, path in paths.items():
    with h5py.File(path, "r") as f:
        ecc = f["samples/eccentricity"][:]
    results[key] = {
        "eccentricity": ecc,
        "median": get_percentile(ecc, 50),
        "lower": get_percentile(ecc, 5),
        "upper": get_percentile(ecc, 95)
    }

# Plot setup
plt.figure(figsize=(7, 7))

x_grid_min = 1e-5
x_grid_max = 0.2
x_grid = np.logspace(np.log10(x_grid_min), np.log10(x_grid_max), 500)

num_hist_bins = 100
hist_bins = np.logspace(np.log10(x_grid_min), np.log10(x_grid_max), num_hist_bins + 1)

for key, res in results.items():
    ecc = res["eccentricity"]

    if key == "teob_log":
        e_min_boundary = 1e-4
        kde_bandwidth_log_ecc = 0.01
    elif key == "seob_log":
        e_min_boundary = 1e-4
        kde_bandwidth_log_ecc = 0.01
    else:
        e_min_boundary = 0.0
        kde_bandwidth_linear_ecc = 0.005

    if key in ["seob_log", "teob_log"]:
        valid_ecc_samples_linear = ecc[ecc >= e_min_boundary]

        if len(valid_ecc_samples_linear) == 0:
            print(f"Warning: No valid eccentricity samples for KDE for {key} after filtering for reflection. Skipping KDE plot.")
            continue

        log_ecc_samples = np.log10(valid_ecc_samples_linear)
        log_e_min_boundary = np.log10(e_min_boundary)
        reflected_log_ecc = (2 * log_e_min_boundary) - log_ecc_samples
        combined_log_ecc = np.concatenate((log_ecc_samples, reflected_log_ecc))
        kde_log = gaussian_kde(combined_log_ecc, bw_method=kde_bandwidth_log_ecc)
        log_x_grid = np.log10(x_grid)
        y_kde_log_raw = kde_log(log_x_grid)
        y_kde_log_raw[log_x_grid < log_e_min_boundary] = 0.0
        y_kde_log_scaled_by_reflection = y_kde_log_raw * 2.0
        y_kde_linear = y_kde_log_scaled_by_reflection / (x_grid * np.log(10))
        area_y_kde_linear = np.trapz(y_kde_linear, x_grid)
        if area_y_kde_linear > 0:
            y_kde_normalized = y_kde_linear / area_y_kde_linear
        else:
            y_kde_normalized = y_kde_linear
            print(f"Warning: Area under KDE for {key} is zero or negative. Not normalizing.")

        label_to_use = labels[key]
        plt.plot(x_grid, y_kde_normalized, color=colors[key], label=label_to_use, linewidth=2, linestyle='--')

    else:
        kde = gaussian_kde(ecc, bw_method=0.2)
        median = res["median"]
        lower = res["lower"]
        upper = res["upper"]
        label_to_use = f"{labels[key]}: $e = {median:.3f}^{{+{upper - median:.3f}}}_{{-{median - lower:.3f}}}$"
        y_kde_raw = kde(x_grid)
        area_kde = np.trapz(y_kde_raw, x_grid)
        if area_kde > 0:
            y_kde_normalized = y_kde_raw / area_kde
        else:
            y_kde_normalized = y_kde_raw
            print(f"Warning: Area under KDE for {key} is zero. Not normalizing.")

        plt.plot(x_grid, y_kde_normalized, color=colors[key], label=label_to_use, linewidth=2)
        plt.axvline(lower, color=colors[key], linestyle='dashed', linewidth=1)
        plt.axvline(median, color=colors[key], linestyle='solid', linewidth=1)
        plt.axvline(upper, color=colors[key], linestyle='dashed', linewidth=1)

plt.xlabel("Eccentricity", fontsize=14)
plt.ylabel("Probability Density", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xscale('linear')
plt.xlim(0,0.2)
plt.ylim(0.0,45)
plt.yscale('linear')
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.show()

for key in results:
    print(f"{labels[key]} 90% CI: [{results[key]['lower']:.2e}, {results[key]['upper']:.2e}]")
