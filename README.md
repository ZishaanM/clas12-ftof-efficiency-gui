# clas12-ftof-efficiency-gui

A small desktop app that turns per-run CLAS12 Forward Time-of-Flight (FTOF) hit counts into paddle-by-paddle efficiencies and plots them, so you don't have to dig through the raw CSVs by hand.

**For reviewers:** Python, CustomTkinter, pandas, matplotlib, SciPy · started as a summer research project; I built the main GUI (earlier drafts, some written with a collaborator, are in `scratch/`)

## Problem

The FTOF detector in CLAS12 (Jefferson Lab, Hall B) has six sectors, three panels (layers), and many scintillator paddles. Efficiency data comes as one long CSV per run, with a "should have fired" and "did fire" count for every paddle and five event topologies. Comparing specific sectors, layers, and topologies across runs by reading those tables is slow and easy to get wrong.

## Approach

- `main.py` is a CustomTkinter window with two tabs. It doesn't do the data work itself; it calls two scripts with `subprocess` and passes the checkbox selections as JSON arguments. That kept the scripts runnable on their own from the command line.
- `MakeData_Jan24.py` splits a run's long CSV by topology, merges the five pieces back together on sector/layer/paddle, and computes an efficiency (`did / should`) and variance for each topology. It writes one wide CSV per run to `output/`.
- `GraphData_Jan24.py` reads that file and draws efficiency vs. paddle number, with error bars from the variance column, for every selected sector/layer/topology combination. Each plot is saved as a PDF in `PDFs/`. The overlay option puts all selected sectors, layers, or topologies on the same plot instead of separate ones.
- The **KS Test** tab runs SciPy's two-sample Kolmogorov–Smirnov test on the efficiencies of two runs to check whether they look like they come from the same distribution.
- Sample data is included under `CSV/` so the app works without access to JLab systems: 128 RGA inbending runs, 66 RGA outbending runs, and 4 RGB Spring 2019 runs.

## How to run

**Prerequisites**

- Python 3 (tested with 3.12) with Tkinter. Tkinter ships with the python.org installers for Windows and macOS; on Debian/Ubuntu install it with `sudo apt install python3-tk`.
- A desktop session. This is a GUI app, so it needs a display.

**Clone and install**

```bash
git clone https://github.com/ZishaanM/clas12-ftof-efficiency-gui.git
cd clas12-ftof-efficiency-gui
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Run the GUI**

```bash
python main.py
```

1. On the **Controller** tab, type a run number that exists under `CSV/` (for example `5032`) and click **Retrieve FTOF Data From Run Number**. This runs `MakeData_Jan24.py` and writes `output/ftof_eff_5032_wide.csv`.
2. Tick one or more sectors, layers, and topologies, optionally pick an overlay setting, and click **Graph FTOF Efficiency Data**. PDFs are written to `PDFs/`.
3. On the **KS Test** tab, enter two run numbers (for example `5032` and `5422`), choose which topology's efficiencies to compare (or `All`), and click **Calculate**. The statistic and p-value appear on the left side of the window. Runs that haven't been processed yet are processed automatically.

**Run the scripts without the GUI**

```bash
python MakeData_Jan24.py 5032
# args: run, sectors, layers, topologies, overlay sectors, overlay layers, overlay topologies
python GraphData_Jan24.py 5032 "[1,2]" "[1]" "[1]" False False False
```

**Verify**

- `MakeData_Jan24.py` prints the input file it read and the output file it wrote.
- `GraphData_Jan24.py` prints one `... .pdf created` line per plot.
- `output/ftof_eff_5032_wide.csv` should have 582 rows and 25 columns.

**Configuration**

Paths are relative to the repo by default. To use data or output folders somewhere else, set any of these environment variables:

| Variable | Default | Used for |
| --- | --- | --- |
| `FTOF_DATA_DIR` | `CSV/` | Per-run inputs, searched as `<dir>/*/*/ftof_eff_<run>.csv` |
| `FTOF_OUTPUT_DIR` | `output/` | Wide per-run CSVs |
| `FTOF_PDF_DIR` | `PDFs/` | Plot PDFs |

**Gotchas**

- Only runs with a per-run file under `CSV/` work. Run numbers outside the bundled sets exit with a "No input file" message.
- The aggregated files (`CSV/rga_all.csv`, `CSV/rga_rgb_all.csv`, etc.) use a different, particle-based column layout and aren't used by the scripts.
- The "Minimum Files Before Graphing" field and the About/Help menus are left over from an earlier design and don't do anything yet.
- The Controller tab handles one retrieve and one graph per session; restart the app to graph another run or selection.

## What's interesting in the code

- `MakeData_Jan24.py`: the topology split/merge, and `calculate_variance`, which adjusts the count by one when a paddle fired every time or never, so those paddles don't get zero variance.
- `GraphData_Jan24.py`: `make_graphs` turns the overlay flags into groups of sectors/layers/topologies and builds one plot per group.

## Stack

Python, CustomTkinter (Tkinter), pandas, NumPy, matplotlib, SciPy
