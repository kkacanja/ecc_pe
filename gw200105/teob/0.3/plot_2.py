import h5py
import numpy as np
import corner
import matplotlib.pyplot as plt

# Define a function to convert log-likelihood ratio to SNR
def snr_from_loglr(loglr):
    # Replace this with the actual conversion formula if necessary
    return np.exp(loglr)  # Example conversion, modify as needed

# Open the HDF5 file and extract the necessary datasets
with h5py.File('result.hdf.checkpoint', 'r') as f:
    # Extract the samples
    mchirp = np.array(f['/samples/mchirp'])
    q = np.array(f['/samples/q'])
    spin1z = np.array(f['/samples/spin1z'])
    spin2z = np.array(f['/samples/spin2z'])
    eccentricity = np.array(f['/samples/eccentricity'])
    anomaly = np.array(f['/samples/anomaly'])
    loglikelihood = np.array(f['/samples/loglikelihood'])
    lognl = np.array(f['/samples/lognl'])  # Assuming this is the normalization

# Compute the log-likelihood ratio (loglr)
loglr = loglikelihood - lognl

# Convert loglr to SNR
snr = snr_from_loglr(loglr)

# Prepare the data for the corner plot, now including eccentricity and anomaly
data = np.vstack([mchirp, q, spin1z, spin2z, eccentricity, anomaly]).T

# Create the corner plot
fig = corner.corner(data, labels=["$\mathcal{M}$", "$q$", "$\chi_1$", "$\chi_2$", "eccentricity", "anomaly"], 
                    show_titles=True, title_args={"fontsize": 12}, 
                    color=plt.cm.viridis(snr / max(snr)))

# Show the plot
plt.show()
