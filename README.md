## 📌 Overview

This is not official resource.

Judge Nitro tasks such as:

- https://judge.nitro-ai.org/competitions/roai-2025/lot-2-2026/3/view
- https://judge.nitro-ai.org/competitions/ceoai/ceoai-2026-practice-2/1/view
- https://judge.nitro-ai.org/competitions/ceoai/ceoai-2026-practice-2/2/view
- https://judge.nitro-ai.org/competitions/nitro/pre-lot-2026/2/view
- https://judge.nitro-ai.org/competitions/nitro/pre-lot-2026/3/view

use `pre_judging_script.py` files that may fail at runtime due to missing dependencies, in particular the absence of a `predictor` library.

These scripts are intended for the official Judge Nitro environment and assume the existence of a `predictor` module, which is not available during local execution. As a result, running them locally can lead to import errors or other runtime issues.

## ✅ Supported Submission Formats

The current version supports the following submission formats:

- `submission.pkl`
- `submission.zip`
- `submission.pt`
- `submission.pth`
- `submission.onnx`
- `submission.npy`
- `submission.npz`
- `submission`
