import os
import json
import gdown
import numpy as np
from scipy.io import loadmat
from task_and_baseline import baseline, build_task_helpers

# Download the dataset
url = "https://drive.google.com/file/d/1BBHVSI4KB-B8OX46eN1Nm4ARCeq6Rui4/view?usp=sharing"
downloaded_file = "challenge.mat"
# Check if the file already exists 
if not os.path.exists(downloaded_file):
    print("Downloading dataset...")
    gdown.download(url, downloaded_file, quiet=False)
else:
    print("Dataset already exists")

data = loadmat("challenge.mat", simplify_cells=True)
tx = data["tx"].astype(np.complex128)
rx = data["rx"].astype(np.complex128)
Fs = float(data["Fs"])
N, _ = tx.shape

tx_n = tx / (np.sqrt(np.mean(np.abs(tx) ** 2, axis=0, keepdims=True)) + 1e-30)
helpers = build_task_helpers(tx_n, Fs, N)


def your_canceller(tx_n, rx):
    """
    Cancellation Pipeline:
    Layer 1: Nonlinear Self-Interference F_c
    Layer 2: Spatially Coherent Interference E
    """
    import numpy as np

    # Self-Interference Removal
    # Used Volterra-series intermodulation model to suppress TX leakage
    tx_interference = helpers["fit_tx_prediction"](rx)
    rx_residual_tx = rx - tx_interference

    # Spatial Feature Extraction
    # Filter residuals to the evaluation band to isolate the external interference E without overfitting to out-of-band noise
    rx_band = np.column_stack([helpers["score_filter"](rx_residual_tx[:, ch]) for ch in range(4)])
    
    # Blind Source Separation via SVD
    # Extract the dominant spatial eigenvector (U[:,0]) - primary wavefront of the spatially coherent interference E
    u, s, vh = np.linalg.svd(rx_band, full_matrices=False)
    E_template = u[:, 0:1] 

    # Phase-Aligned Projection and Regularization
    # Project the common-mode interference onto each RX channel individually to account for phase shifts across the multi-antenna array.
    E_hat_full = np.zeros_like(rx_residual_tx)
    for ch in range(4):
        target = rx_residual_tx[:, ch:ch+1]
        # Align amplitude and phase for each antenna
        w, _, _, _ = np.linalg.lstsq(E_template, target, rcond=None)
        # Apply 0.80 safety coefficient
        E_hat_full[:, ch:ch+1] = E_template @ (w * 0.8) 
    # Signals s_c after suppressing I_tx and E
    return rx_residual_tx - E_hat_full


print("\n=== Baseline ===")
baseline_reds, baseline_avg = helpers["score"](
    rx, baseline(tx_n, rx, helpers["fit_tx_prediction"]), label="baseline"
)

print("=== Your Solution ===")
yours_reds, yours_avg = helpers["score"](rx, your_canceller(tx_n, rx), label="yours")

results = {
    "baseline": {
        "per_channel_db": baseline_reds,
        "average_db": baseline_avg,
    },
    "yours": {
        "per_channel_db": yours_reds,
        "average_db": yours_avg,
    },
}

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
