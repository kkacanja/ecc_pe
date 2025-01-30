import h5py
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import os
from collections import defaultdict

# Seaborn theme
sns.set_theme(style="whitegrid")

# File paths categorized by waveform type
waveform_files = {
    "gw200115": {
        "teob": ["/home/kkacanja/ecc_pe/gw200115/teob/result.hdf"],
        "teobHM": ["/home/kkacanja/ecc_pe/gw200115/teobHM/result_scratchy.hdf"],
        "seob": ["/home/kkacanja/ecc_pe/gw200115/seob/result.hdf"],
        "seobHM": ["/home/kkacanja/ecc_pe/gw200115/seobHM/result_allmodes.hdf"],
    },
    "gw190814": {
        "teob": ["/home/kkacanja/ecc_pe/gw190814/teob/result.hdf"],
        "seob": ["/home/kkacanja/ecc_pe/gw190814/seob/result.hdf.bkup"],
        "seobHM": ["/home/kkacanja/ecc_pe/gw190814/seobHM/result.hdf.bkup"],
        "teobHM": ["/home/kkacanja/ecc_pe/gw190814/teobHM/result.hdf"],
    },
    "gw200105":{
         "seob": ["/home/kkacanja/ecc_pe/gw200105/seob/0.3/final/result.hdf.bkup"],
         "teob": ["/home/kkacanja/ecc_pe/gw200105/teob/0.3/final/result.hdf.bkup"],
         "seobHM": ["/home/kkacanja/ecc_pe/gw200105/seobHM/0.3/final/result.hdf.bkup"],
         "teobHM": ["/home/kkacanja/ecc_pe/gw200105/seob/0.3/final/result.hdf.bkup"],
     },
    "gw190425": {
        "teob": ["/home/kkacanja/ecc_pe/gw190425/teob/result.hdf"],
        "seob": ["/home/kkacanja/ecc_pe/gw190425/seob/result.hdf"],
        "seobHM": ["/home/kkacanja/ecc_pe/gw190425/seobHM/result.hdf"],
        "teobHM": ["/home/kkacanja/ecc_pe/gw190425/teobHM/result.hdf"],
    },
    "gw170817": {
        "teob": ["/home/kkacanja/ecc_pe/gw170817/teob/result.hdf"],
        "seob": ["/home/kkacanja/ecc_pe/gw170817/seob/result.hdf"],
        "seobHM": ["/home/kkacanja/ecc_pe/gw170817/seobHM/result.hdf"],
        "teobHM": ["/home/kkacanja/ecc_pe/gw170817/teobHM/result.hdf"],
    },
    "gw230529": {
        "teob": ["/home/kkacanja/ecc_pe/gw230529/teob/result.hdf"],
        "seob": ["/home/kkacanja/ecc_pe/gw230529/seob/result.hdf"],
        "seobHM": ["/home/kkacanja/ecc_pe/gw230529/seobHM/result.hdf"],
        "teobHM": ["/home/kkacanja/ecc_pe/gw230529/teobHM/result.hdf"],
    },

}


# Parameter labels
parameters = {
    "mchirp": "Chirp Mass",
    "q": "Mass Ratio",
    "eccentricity": "Eccentricity",
    "anomaly": "Anomaly",
    "rel_anomaly": "Relative Anomaly"
}

# Output directory
output_dir = "/home/kkacanja/public_html/ecc_pe/plots/"
os.makedirs(output_dir, exist_ok=True)

# Colors for different models
model_colors = {
    "teob": "blue",
    "teobHM": "cyan",
    "seob": "orange",
    "seobHM": "red"
}

# Helper function to plot KDE and annotate credible intervals
def plot_kde_with_intervals(ax, data, param_label, color, label_suffix, median, lower_error, upper_error):
    kde = gaussian_kde(data)
    x_vals = np.linspace(min(data), max(data), 1000)
    y_vals = kde(x_vals)
    ax.plot(x_vals, y_vals, label=f"{param_label} ({label_suffix}: Median = {median:.3f}, +{upper_error:.3f}, -{lower_error:.3f})", color=color)
    ax.axvline(median, color=color, linestyle="-", alpha=0.7)
    ax.axvline(median - lower_error, color=color, linestyle="--", alpha=0.7)
    ax.axvline(median + upper_error, color=color, linestyle="--", alpha=0.7)

# Generate plots for each source
for source_name, models in waveform_files.items():
    # Determine the number of valid parameters to plot
    valid_params = []
    for param in parameters.keys():
        for model, file_list in models.items():
            for file in file_list:
                with h5py.File(file, "r") as f:
                    if param in f["samples"]:
                        valid_params.append(param)
                        break
    
    valid_params = list(set(valid_params))  # Remove duplicates

    # Create subplots dynamically
    num_params = len(valid_params)
    ncols = 2
    nrows = (num_params + ncols - 1) // ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 5 * nrows))
    axs = axs.flatten()

    for idx, param in enumerate(valid_params):
        for model, file_list in models.items():
            for file in file_list:
                with h5py.File(file, "r") as f:
                    if param in f["samples"]:
                        data = f[f"samples/{param}"][:]
                        lower, median, upper = np.percentile(data, [5, 50, 95])
                        lower_error = median - lower
                        upper_error = upper - median
                        plot_kde_with_intervals(axs[idx], data, parameters[param], model_colors[model], model.upper(), median, lower_error, upper_error)
        axs[idx].legend()

    # Remove empty subplots
    for ax in axs[num_params:]:
        fig.delaxes(ax)

    # Adjust layout and save the plot
    fig.suptitle(f"Comparison for {source_name}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    output_file = os.path.join(output_dir, f"{source_name}_comparison.png")
    plt.savefig(output_file, dpi=300)
    plt.close(fig)

print(f"Plots saved to {output_dir}")
