# SMILES-2026 Signal Interference Cancellation

Reproducibility instructions: exact commands to run your solution and acquire the same results.json, required environment (if any), and any important implementation details needed to reproduce your result.
Final solution description: What components you modified ? What your final approach is ? Why you made these choices ? What contributed most to improving the metric ?
------------------------------------------------------------------------------------------------------------------------------------------------------------
## How to run
Create an environment with Python 3 and install the required packages:
pip install numpy scipy
------------------------------------------------------------------------------------------------------------------------------------------------------------



# 2-Layer Mathematical Approach: Least Squares Regression

## Problem
your_canceller function focuses on removing structured interference I[n, c] = F_c( TX )  +  E[n, c],
where
* F_c(·) is an unknown nonlinear function of all transmitted signals jointly, depends on cross-products between different TX channels.
* E[n, c] is a spatially-coherent external interference term, shared across all 4 RX channels.

## Layer 1: Least Squares Regression
The desired signal s is uncorrelated with TX.
Find the weights that minimize the difference between XW and RX

##

# Wrong models
## Fourier Transform Filtering
Why it didn't work: removes everything at the specified frequency.

Experiments and failed attempts: What ideas you tried but did not include in the final solution ? Why they did not work or were discarded ?