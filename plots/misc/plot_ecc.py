import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Path to your HDF5 file
file_path = "/home/kkacanja/ecc_pe/gw200105/teob/0.3/result.hdf.bkup"
#file_path = "result.hdf.bkup"

# Open the HDF5 file
with h5py.File(file_path, 'r') as f:
    # Load the eccentricity dataset
    eccentricity = f['/samples/eccentricity'][:]

# Calculate the eccentricity value at 90% confidence
eccentricity_90 = np.percentile(eccentricity, 90)

# Plot histogram of the eccentricity samples
plt.hist(eccentricity, bins=50, density=True, alpha=0.6, color='g', label='Eccentricity Samples')

# Fit a Gaussian to the data
mu, std = norm.fit(eccentricity)

# Plot the Gaussian fit
x = np.linspace(min(eccentricity), max(eccentricity), 1000)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2, label=f'Gaussian Fit (μ={mu:.3f}, σ={std:.3f})')

# Highlight the 90% confidence eccentricity value
plt.axvline(eccentricity_90, color='r', linestyle='--', label=f'90% Eccentricity: {eccentricity_90:.3f}')
plt.fill_between(x, p, where=(x <= eccentricity_90), color='gray', alpha=0.3, label='Area ≤ 90%')

# Customize the plot
plt.title("Eccentricity Parameter Estimation")
plt.xlabel("Eccentricity")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Print the 90% confidence eccentricity value
print(f"Eccentricity value with 90% confidence: {eccentricity_90:.3f}")

plt.savefig('/home/kkacanja/public_html/ecc_pe/90_confidence_105.png')
