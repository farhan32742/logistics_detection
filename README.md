# Logistics Detection

This repository contains code and model weights for an object detection project used in logistics workflows.

Included
- `best.pt` — trained model weights (kept in repo intentionally).
- `main.py` — main entrypoint for inference/training.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — container definition.

Quick start

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. Run inference or training (example):

```powershell
python main.py
```

Notes
- The file `best.pt` (~18.9 MB) is included in the repository. If you prefer to keep large models outside the git history, consider using Git LFS.
- The `.gitignore` is configured to ignore `*.pt` files but explicitly keeps `best.pt`.

License
- Add a license file if you want this project published under a specific license.

Contact
- Open an issue or contact the repository owner on GitHub.
