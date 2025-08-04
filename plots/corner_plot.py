import numpy as np
import h5py
import corner
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde

# Parameter setup - Keep all 6 parameters
param_labels = [
    r"$\mathcal{M}$",
    r"$q$",
    r"$e_{20}$",
    r"$\chi_{1z}$",
    r"$\chi_{2z}$",
    r"$\ell$"
]
param_names_teob = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "anomaly"]
param_names_seob = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "rel_anomaly"]
param_names_teobHM = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "anomaly"]
param_names_seobHM = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "rel_anomaly"]
param_names_comp = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "rel_anomaly"]
param_names_morras = ["mchirp", "q", "eccentricity", "spin1z", "spin2z", "rel_anomaly"]

# File paths
teob_file = "/home/kkacanja/ecc_pe/gw200105/teob/workflow/pos.hdf"
seob_file = "/home/kkacanja/ecc_pe/gw200105/seob/workflow/pos.hdf"
teobHM_file = "/home/kkacanja/ecc_pe/gw200105/teobHM/workflow/pos.hdf"
seobHM_file = "/home/kkacanja/ecc_pe/gw200105/seobHM/workflow/pos.hdf"
planes_file = "/home/kkacanja/ecc_pe/gw200105/comparisons/converted_posteriors_pycbc_format.hdf"
morras_file = "/home/kkacanja/ecc_pe/gw200105/comparisons/converted_posteriors_pycbc_format_morras.hdf"

# Corrected load_samples function
def load_samples(fname, param_names):
    with h5py.File(fname, "r") as f:
        data_columns = []
        for p in param_names:
            try:
                data_columns.append(f[f"samples/{p}"][:])
            except KeyError:
                print(f"Error: Parameter '{p}' not found in '{fname}'. Please check the HDF5 structure.")
                raise
        return np.vstack(data_columns).T

# Load samples
teob_samples = load_samples(teob_file, param_names_teob)
seob_samples = load_samples(seob_file, param_names_seob)
teobHM_samples = load_samples(teobHM_file, param_names_teobHM)
seobHM_samples = load_samples(seobHM_file, param_names_seobHM)
planes_samples = load_samples(planes_file, param_names_comp)
morras_samples = load_samples(morras_file, param_names_morras)

# Store all samples in a dictionary for easier iteration
all_samples = {
    "teob": teob_samples,
    "seob": seob_samples,
    "teobHM": teobHM_samples,
    "seobHM": seobHM_samples,
    "planes": planes_samples,
    "morras": morras_samples
}

# --- Data Diagnostics (kept for verification) ---
print("\n--- Data Diagnostics ---")
print(f"\nTEOB Samples:\n Eccentricity (column 2): min={np.min(teob_samples[:, 2])}, max={np.max(teob_samples[:, 2])}, unique={len(np.unique(teob_samples[:, 2]))}")
print(f" Anomaly (column 5): min={np.min(teob_samples[:, 5])}, max={np.max(teob_samples[:, 5])}, unique={len(np.unique(teob_samples[:, 5]))}")
print(f"\nSEOB Samples:\n Eccentricity (column 2): min={np.min(seob_samples[:, 2])}, max={np.max(seob_samples[:, 2])}, unique={len(np.unique(seob_samples[:, 2]))}")
print(f" Rel_anomaly (column 5): min={np.min(seob_samples[:, 5])}, max={np.max(seob_samples[:, 5])}, unique={len(np.unique(seob_samples[:, 5]))}")
print(f"\nTEOBHM Samples:\n Eccentricity (column 2): min={np.min(teobHM_samples[:, 2])}, max={np.max(teobHM_samples[:, 2])}, unique={len(np.unique(teobHM_samples[:, 2]))}")
print(f" Anomaly (column 5): min={np.min(teobHM_samples[:, 5])}, max={np.max(teobHM_samples[:, 5])}, unique={len(np.unique(teobHM_samples[:, 5]))}")
print(f"\nSEOBHM Samples:\n Eccentricity (column 2): min={np.min(seobHM_samples[:, 2])}, max={np.max(seobHM_samples[:, 2])}, unique={len(np.unique(seobHM_samples[:, 2]))}")
print(f" Rel_anomaly (column 5): min={np.min(seobHM_samples[:, 5])}, max={np.max(seobHM_samples[:, 5])}, unique={len(np.unique(seobHM_samples[:, 5]))}")
print(f"\nPlanes Samples:\n Eccentricity (column 2): min={np.min(planes_samples[:, 2])}, max={np.max(planes_samples[:, 2])}, unique={len(np.unique(planes_samples[:, 2]))}")
print(f" Rel_anomaly (column 5): min={np.min(planes_samples[:, 5])}, max={np.max(planes_samples[:, 5])}, unique={len(np.unique(planes_samples[:, 5]))}")
print(f"\nmorras Samples:\n Eccentricity (column 2): min={np.min(morras_samples[:, 2])}, max={np.max(morras_samples[:, 2])}, unique={len(np.unique(morras_samples[:, 2]))}")
print(f" Rel_anomaly (column 5): min={np.min(morras_samples[:, 5])}, max={np.max(morras_samples[:, 5])}, unique={len(np.unique(morras_samples[:, 5]))}")
print("--- End of Data Diagnostics ---")

# Define ranges for corner plot
num_params = len(param_labels)
ranges_for_plot = []
for i in range(num_params):
    all_data_for_param = np.concatenate([
        teob_samples[:, i],
        seob_samples[:, i],
        teobHM_samples[:, i],
        seobHM_samples[:, i],
        planes_samples[:, i],
        morras_samples[:, i]
    ])
    all_data_for_param = all_data_for_param[np.isfinite(all_data_for_param)]
    if len(all_data_for_param) > 0:
        min_val = np.min(all_data_for_param)
        max_val = np.max(all_data_for_param)
    else:
        min_val, max_val = 0.0, 1.0

    if i == 2:  # Eccentricity
        if min_val == 0.0 and max_val == 0.0:
            ranges_for_plot.append((-0.001, 0.001))
        else:
            ranges_for_plot.append((0.0, 0.2))
    elif i == 5:  # Anomaly / Rel_anomaly
        ranges_for_plot.append((0.0, 2 * np.pi))
    else:
        buffer = (max_val - min_val) * 0.08
        if buffer == 0:
            ranges_for_plot.append((min_val - 0.01, min_val + 0.01))
        else:
            ranges_for_plot.append((min_val - buffer, max_val + buffer))

# Colors
model_colors = {
    "teob": "orange",
    "seob": "#024CAA",
    "teobHM": "red",
    "seobHM": "green",
    "planes": "#FF76E1",  # PINK
    "morras": "#AE78C3"  # PURPLE
}

# --- Custom plotting function for 1D histograms ---
def plot_1d_histogram(ax, x, **kwargs):
    color = kwargs.get('color', 'black')
    smooth = kwargs.get('smooth', 1.0)
    weights = kwargs.get('weights', None)

    x = x[np.isfinite(x)]
    if len(x) == 0:
        return

    if weights is not None:
        weights = weights[np.isfinite(x)]

    if len(np.unique(x)) == 1:
        ax.axvline(x[0], color=color, linestyle='-', linewidth=kwargs.get('lw', 1.0) * 1.5)
        return

    kde = gaussian_kde(x, weights=weights) if weights is not None else gaussian_kde(x)

    x_min, x_max = ax.get_xlim()
    kde_eval_x = np.linspace(x_min, x_max, 500)
    pdf_kde = kde.evaluate(kde_eval_x)

    ax.fill_between(kde_eval_x, 0, pdf_kde, color=color, alpha=0.2)
    ax.plot(kde_eval_x, pdf_kde, color=color, linewidth=kwargs.get('lw', 1.0))

# --- Corner Plotting ---
fig = plt.figure(figsize=(12, 12))

# Plot TEOB first (behind)
fig = corner.corner(
    teob_samples,
    labels=param_labels,
    label_kwargs={"fontsize": 14},
    color=model_colors["teob"],
    bins=35,
    smooth=1.4,
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.2, "linestyles": "dashdot"},
    quantiles=[],
    levels=[0.9],
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Overlay Planes et al.
corner.corner(
    planes_samples,
    fig=fig,
    color=model_colors["planes"],
    bins=35,
    smooth=2.0,
    quantiles=[],
    levels=[0.9],
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.3, "linestyles": "dotted"},
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Overlay morras et al.
corner.corner(
    morras_samples,
    fig=fig,
    color=model_colors["morras"],
    bins=35,
    smooth=2.0,
    quantiles=[],
    levels=[0.9],
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.2, "linestyles": "dashed"},
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Overlay TEOBHM
corner.corner(
    teobHM_samples,
    fig=fig,
    color=model_colors["teobHM"],
    bins=35,
    smooth=1.4,
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.2, "linestyles": "dashdot"},
    quantiles=[],
    levels=[0.9],
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Overlay SEOBHM
corner.corner(
    seobHM_samples,
    fig=fig,
    color=model_colors["seobHM"],
    bins=35,
    smooth=2.0,
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.0, "linestyles": "-"},
    quantiles=[],
    levels=[0.9],
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Overlay SEOB (on top)
corner.corner(
    seob_samples,
    fig=fig,
    color=model_colors["seob"],
    bins=35,
    smooth=2.0,
    hist_kwargs={"density": True},
    contour_kwargs={"linewidths": 1.0},
    quantiles=[],
    levels=[0.9],
    show_titles=False,
    show_scatter=False,
    plot_datapoints=False,
    plot_density=False, # No 2D shading
    plot_contours=True,
    range=ranges_for_plot,
    plot_fn=plot_1d_histogram
)

# Adjust margins for titles and overall layout
plt.subplots_adjust(top=0.88)
axes = np.array(fig.axes).reshape(len(param_labels), len(param_labels))

# Helper to get label string
def get_label(i):
    if i == 2:
        return r"e_{20}"
    else:
        return param_labels[i].strip("$")

# Calculate max density for each parameter across all models for Y-axis limits
max_y_densities = np.zeros(num_params)
for i in range(num_params):
    current_max_density = 0.0
    for model_name, samples in all_samples.items():
        data = samples[:, i]
        data = data[np.isfinite(data)]
        if len(data) == 0 or len(np.unique(data)) == 1:
            continue
        kde = gaussian_kde(data, bw_method='scott') # Use default bandwidth method
        x_eval = np.linspace(np.min(data), np.max(data), 500)
        if len(x_eval) > 1:
            pdf_kde = kde.evaluate(x_eval)
            current_max_density = max(current_max_density, np.max(pdf_kde))
    max_y_densities[i] = current_max_density

# Hardcoded eccentricity error values, plotting KDE is distorting the values
ecc_error_values = {
    "seobHM": {"med": 0.125, "em": 0.082, "ep": 0.029},
    "teobHM": {"med": 0.135, "em": 0.088, "ep": 0.019},
    "teob": {"med": 0.137, "em": 0.092, "ep": 0.021},
    "seob": {"med": 0.139, "em": 0.092, "ep": 0.020},
    "morras": {"med": 0.145, "em": 0.097, "ep": 0.007},
}


# Add titles with median and 1-sigma intervals and set Y-limits for diagonal plots
for i in range(len(param_labels)):
    ax = axes[i, i]
    ax.set_title("") # Clear default corner title

    # Set Y-axis limit for the diagonal plots
    if max_y_densities[i] > 0:
        ax.set_ylim(0, max_y_densities[i] * 1.2) # 10% buffer
    else:
        ax.set_ylim(0, 1) # Default small limit if no density

    def extract_stats(samples_array, param_index, model_name=None):
        # Handle eccentricity with hardcoded values
        if param_index == 2 and model_name in ecc_error_values:
            stats = ecc_error_values[model_name]
            return stats["med"], stats["em"], stats["ep"]

        # Original calculation for other parameters or models not in hardcoded list
        data = samples_array[:, param_index]
        if len(np.unique(data)) == 1:
            val = data[0]
            return val, 0.0, 0.0
        med = np.median(data)
        lower = np.percentile(data, 16)
        upper = np.percentile(data, 84)
        return med, med - lower, upper - med

    label = get_label(i)

    # morras et al. (bottom title)
    m, em, ep = extract_stats(morras_samples, i, "morras")
    ax.text(0.5, 1.05, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["morras"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    # Planes et al.
    m, em, ep = extract_stats(planes_samples, i, "planes")
    ax.text(0.5, 1.15, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["planes"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    # TEOBHM
    m, em, ep = extract_stats(teobHM_samples, i, "teobHM")
    ax.text(0.5, 1.25, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["teobHM"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    # SEOBHM
    m, em, ep = extract_stats(seobHM_samples, i, "seobHM")
    ax.text(0.5, 1.35, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["seobHM"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    # TEOB
    m, em, ep = extract_stats(teob_samples, i, "teob")
    ax.text(0.5, 1.45, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["teob"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    # SEOB (top title)
    m, em, ep = extract_stats(seob_samples, i, "seob")
    ax.text(0.5, 1.55, rf"${label} = {m:.2f}^{{+{ep:.2f}}}_{{-{em:.2f}}}$", color=model_colors["seob"], fontsize=8, ha='center', va='bottom', transform=ax.transAxes)

    ax.tick_params(axis='both', which='major', labelsize=10)

# Adjust all axes labels
for ax in fig.axes:
    ax.xaxis.label.set_size(14)
    ax.yaxis.label.set_size(14)

# Legend elements
legend_elements = [
    Line2D([0], [0], color=model_colors["seob"], lw=1.4, label='SEOBNRv5EHM ((2,2) mode)'),
    Line2D([0], [0], color=model_colors["teob"], lw=1.2, linestyle='dashdot', label='TEOBResumS-DALI ((2,2) mode)'),
    Line2D([0], [0], color=model_colors["seobHM"], lw=1.0, label='SEOBNRv5HM (HOM)'),
    Line2D([0], [0], color=model_colors["teobHM"], lw=1.2, linestyle='dashdot', label='TEOBResumS-DALI (HOM)'),
    Line2D([0], [0], color=model_colors["planes"], lw=1.4, linestyle="dotted", label='Planes et al'),
    Line2D([0], [0], color=model_colors["morras"], lw=1.2, linestyle="dashed", label='Morras et al')
]

fig.legend(handles=legend_elements, loc='upper right', fontsize=10, bbox_to_anchor=(0.99, 0.99))

plt.close()
