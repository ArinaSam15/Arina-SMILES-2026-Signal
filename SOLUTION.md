# SMILES-2026 Signal Interference Cancellation
------------------------------------------------------------------------------------------------------------------------------------------------------------
## How to run
Create a virtual environment with Python 3 and install the required packages:
pip install numpy scipy gdown

After that run the script in the terminal:
python applicant_solution.py

The script will download the dataset challenge.mat.

## Obtained results:
  * ch0: 10.18 dB
  * ch1: 7.66 dB
  * ch2: 12.48 dB
  * ch3: 6.54 dB
  * Metric [yours]: 9.21 dB
------------------------------------------------------------------------------------------------------------------------------------------------------------
## Problem
your_canceller function focuses on removing structured interference I[n, c] = F_c(TX)  +  E[n, c] where
* F_c(·) is an unknown nonlinear function of all transmitted signals jointly, depends on cross-products between different TX channels.
It is self-interference where TX signal leaks into RX path.
* E[n, c] is a spatially-coherent external interference term, shared across all 4 RX channels.

## Solution description
### Layer 1: Nonlinear Self-Interference F_c
Volterra-series model (3rd-order intermodulation terms) constructs a basis for the leakage of the transmit signal
We solve the least-squares problem: min|RX-XW|^2 and thus remove the structured interference driven by known transmit data.

### Layer 2: Spatially Coherent Interference E
The remaining residual contains an external interference term E that is unknown but spatially coherent across all 4 antennas.
1. Used Singular Value Decomposition (SVD) on the band-limited signal to extract the dominant spatial eigenvector.
2. Employed a per-channel Least Squares Projection to align the template's phase and amplitude to each specific antenna. Without phase alignment, the correction added noise.
3. Applied a 0.80 safety coefficient to the final subtraction. Without the safety coefficient, the solution violated the project's "Unexplained-to-Residual" power constraints.
------------------------------------------------------------------------------------------------------------------------------------------------------------
## Failed Attempts
### Fourier Transform Filtering
It removed everything including signal at the specified frequency.
Solution: time-domain regression.
### Simple Mean
It ignored phase shifts between antennas, leading to destructive interference.
Solution: SVD + Complex Weight projection.
### Raw SVD
Overfitted to out-of-band noise.
Solution: score_filter -> SVD extraction.
### High Subtraction
Triggered the unexplained/residual > 0.80.
Solution: introduced a $0.80$ safety factor.
## Implementation Details
1. Used np.linalg.lstsq with rcond=None for numerical robustness on complex-valued signal data.
2. Implemented a local check for challenge.mat to prevent redundant downloads and handled gdown exceptions for reliable dataset acquisition.
