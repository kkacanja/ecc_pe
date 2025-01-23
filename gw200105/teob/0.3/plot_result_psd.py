import h5py
import numpy as np
import matplotlib.pyplot as plt
from pycbc.types import FrequencySeries

# Path to your HDF file
hdf_file = "/home/kkacanja/ecc_pe/gw200105/teob/0.3/result.hdf.bkup"

# Load the stilde dataset for L1
with h5py.File(hdf_file, 'r') as f:
    stilde_data = f['/data/L1/stilde'][:]
    delta_f = 1.0 / 1024  # Adjust this based on your segment length and sampling rate
    freqs = np.arange(len(stilde_data)) * delta_f

# Convert to a FrequencySeries for consistency with PyCBC
stilde = FrequencySeries(stilde_data, delta_f=delta_f)

# Plot the amplitude of stilde
plt.figure(figsize=(10, 6))
plt.plot(freqs, np.abs(stilde), label="L1 Stilde Amplitude")
plt.xlim(20, 1024)  # Limit frequency range to a reasonable range (adjust as needed)
#plt.ylim(1e-25, 1e-21)  # Adjust amplitude range for better visualization
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Frequency-Domain Strain (Stilde) for L1")
plt.legend()
plt.grid()
plt.show()
plt.savefig("/home/kkacanja/public_html/ecc_pe/psd_l1_gw200105.png")
