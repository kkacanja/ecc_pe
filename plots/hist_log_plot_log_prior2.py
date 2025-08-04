import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# File paths
paths = {
    "teob_log": "/home/kkacanja/ecc_pe/gw200105/teob/workflowlog/pos.hdf",
    "teob_uniform": "/home/kkacanja/ecc_pe/gw200105/teob/workflow4/pos.hdf",
    "seob_uniform": "/home/kkacanja/ecc_pe/gw200105/seob/workflow4/pos.hdf",
    "seob_log": "/home/kkacanja/ecc_pe/gw200105/seob/workflowlog/pos.hdf"
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

# Function to calculate percentiles (already assuming auto-reweighted data)
def get_percentile(data, percentile):
    """
    Calculates percentiles for 'auto-reweighted' data.
    Equivalent to np.percentile when data is already a sample from the target distribution.
    """
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

# Define a broader grid for plotting to ensure KDE is evaluated well
# Start from a very small epsilon for log scale
x_grid_min = 1e-5 # Slightly below 10^-4 for visualization
x_grid_max = 0.2
x_grid = np.logspace(np.log10(x_grid_min), np.log10(x_grid_max), 500)

# Define consistent bins for histograms for all plots
# Using log-spaced bins for histograms when x-axis is log-scale is generally better
num_hist_bins = 100
hist_bins = np.logspace(np.log10(x_grid_min), np.log10(x_grid_max), num_hist_bins + 1)


for key, res in results.items():
    ecc = res["eccentricity"]

    # Determine specific e_min for log runs and bandwidths
    if key == "teob_log":
        e_min_boundary = 1e-4
        # Bandwidth for KDE on log-transformed data.
        # This will be in log10(e) space, so values will be smaller.
        # 'scott' or 'silverman' can be good starting points, or tune manually.
        kde_bandwidth_log_ecc = 0.01 # Adjusted for log10(e) scale
    elif key == "seob_log":
        e_min_boundary = 1e-4
        kde_bandwidth_log_ecc = 0.01 # Adjusted for log10(e) scale
    else: # For uniform runs (still use linear KDE as before)
        e_min_boundary = 0.0 # Physical boundary for uniform runs (or effective lower limit)
        kde_bandwidth_linear_ecc = 0.005 # Adjusted to sharpen peaks for uniform runs


    if key in ["seob_log", "teob_log"]:
        # --- KDE on Log-Transformed Eccentricity with Reflection ---
        # Only use eccentricities >= e_min_boundary for log transformation
        valid_ecc_samples_linear = ecc[ecc >= e_min_boundary]
        
        if len(valid_ecc_samples_linear) == 0:
            print(f"Warning: No valid eccentricity samples for KDE for {key} after filtering for reflection. Skipping KDE plot.")
            continue

        # Transform to log10 space
        log_ecc_samples = np.log10(valid_ecc_samples_linear)
        log_e_min_boundary = np.log10(e_min_boundary)

        # Create reflected samples in log10 space
        # Reflection in log space: log_boundary - (log_x - log_boundary) = 2*log_boundary - log_x
        reflected_log_ecc = (2 * log_e_min_boundary) - log_ecc_samples
        
        # Combine original and reflected samples in log10 space
        combined_log_ecc = np.concatenate((log_ecc_samples, reflected_log_ecc))
        
        # Initialize KDE in log10 space
        kde_log = gaussian_kde(combined_log_ecc, bw_method=kde_bandwidth_log_ecc)
        
        # Evaluate KDE over the log-transformed x_grid for plotting
        log_x_grid = np.log10(x_grid) # Ensure x_grid is also log-transformed for evaluation
        y_kde_log_raw = kde_log(log_x_grid)
        
        # Apply boundary condition in log space: density should be zero below log_e_min_boundary
        y_kde_log_raw[log_x_grid < log_e_min_boundary] = 0.0
        
        # --- Crucial Normalization and Transformation from p(log e) to p(e) ---
        # 1. Scale by 2.0 for reflection in log space
        y_kde_log_scaled_by_reflection = y_kde_log_raw * 2.0

        # 2. Transform the PDF from p(log e) to p(e) using the Jacobian: p(e) = p(log e) * d(log e)/de
        # d(log e)/de = d(ln e / ln 10)/de = 1 / (e * ln 10)
        # So, p(e) = p(log10 e) / (e * ln 10) (if p(log e) is density for log base 10)
        # However, scipy.stats.gaussian_kde works on the samples directly,
        # so if the input to KDE is log(x), the output is p(log x).
        # To get p(x), we need p(x) = p(log x) / (dx/d(log x)) = p(log x) / (x * ln(10)) for log10
        # This means, we divide by (x_grid * np.log(10))
        # Note: Be careful with x_grid == 0, though our x_grid starts from 1e-5.
        y_kde_linear = y_kde_log_scaled_by_reflection / (x_grid * np.log(10))

        # Final normalization to ensure the plotted curve integrates exactly to 1 (within numerical precision)
        area_y_kde_linear = np.trapz(y_kde_linear, x_grid)
        if area_y_kde_linear > 0:
            y_kde_normalized = y_kde_linear / area_y_kde_linear
        else:
            y_kde_normalized = y_kde_linear
            print(f"Warning: Area under KDE for {key} is zero or negative. Not normalizing.")

        label_to_use = labels[key]
        plt.plot(x_grid, y_kde_normalized, color=colors[key], label=label_to_use, linewidth=2, linestyle='--')
        
    else: # For uniform runs (keep linear KDE)
        kde = gaussian_kde(ecc, bw_method=0.2) #kde_bandwidth_linear_ecc)
        
        median = res["median"]
        lower = res["lower"]
        upper = res["upper"]
        
        label_to_use = f"{labels[key]}: $e = {median:.3f}^{{+{upper - median:.3f}}}_{{-{median - lower:.3f}}}$"
        
        y_kde_raw = kde(x_grid)
        
        # General normalization for all KDEs if their plot range isn't their full support
        area_kde = np.trapz(y_kde_raw, x_grid)
        if area_kde > 0:
            y_kde_normalized = y_kde_raw / area_kde
        else:
            y_kde_normalized = y_kde_raw
            print(f"Warning: Area under KDE for {key} is zero. Not normalizing.")

        plt.plot(x_grid, y_kde_normalized, color=colors[key], label=label_to_use, linewidth=2)
        
        # Plot percentile lines
        plt.axvline(lower, color=colors[key], linestyle='dashed', linewidth=1)
        plt.axvline(median, color=colors[key], linestyle='solid', linewidth=1)
        plt.axvline(upper, color=colors[key], linestyle='dashed', linewidth=1)

    # --- Overlay unweighted histogram of eccentricity ---
    # Use log-spaced bins for the histogram as well, as the x-axis is log-scaled
    hist_range_start = e_min_boundary if key in ["seob_log", "teob_log"] else x_grid_min
    
    #plt.hist(
     #   ecc, bins=hist_bins, # Use log-spaced bins
      #  range=(hist_range_start, x_grid_max), # Ensure range aligns with actual plot limits
       # weights=None, # Explicitly set weights to None for unweighted histogram
       # density=True, # Normalize histogram to form a probability density
       # color=colors[key], alpha=0.3, histtype='stepfilled'
#    )


plt.xlabel("Eccentricity", fontsize=14)
plt.ylabel("Probability Density", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xscale('linear') # Keep log scale for x-axis
plt.xlim(0,0.2)
plt.ylim(0.0,45)
plt.yscale('linear')
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.savefig("/home/kkacanja/public_html/ecc_pe/plots/eccentricity_kde_posterior_combined_with_hist_logscale_corrected_norm_linear.png")
plt.show()

# Print summary
for key in results:
    print(f"{labels[key]} 90% CI: [{results[key]['lower']:.2e}, {results[key]['upper']:.2e}]")
