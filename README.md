# OrbitVis – LEO Pass Predictor (Python)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Working-success)

A Python tool that fetches live Two-Line Element (TLE) data and predicts satellite visibility passes (AOS/LOS, max elevation, duration) for a ground station (London).

This project was built to strengthen applied orbital mechanics and satellite operations modelling skills.

---

## Features

- Live TLE-based orbit propagation (Skyfield)
- Ground-station visibility prediction
- Automatic AOS/LOS detection
- Maximum elevation & pass duration calculation
- CSV export of pass schedule
- Elevation vs time visualisation

---

## Example Output

![Elevation plot](assets/elevation_plot.png)

---

## Quickstart (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python orbit_pass_predictor.py

```
## Quickstart (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python orbit_pass_predictor.py

```
