# Disk Management & Storage Analyzer

## Features
- Physical drive info (model, type, connection, capacity).
- Partition details (usage, type, space).
- Recursive folder/file scan with category breakdown (Videos, Apps, etc.).
- Top 10 largest folders.
- Visuals: Pie chart (categories), Bar chart (top folders), Treemap (HTML).
- Basic health status.

## Setup
1. `python -m venv .venv`
2. `.venv/Scripts/activate` (Windows)
3. `pip install -r requirements.txt`

## Usage
```
python main.py
```
- Enter path to scan (e.g., `C:/` or `C:/Users`).
- View console output + generated PNG/HTML charts.

## Screenshots
(Add after testing)

## Tech Stack
- Python, psutil, WMI, matplotlib, plotly.

## Performance Notes
- Scans limited to depth 3 for speed; adjust `max_depth` in analyzer.py.
- Skip system folders for access issues.

