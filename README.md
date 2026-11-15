# search-algorithms-benchmark

Linear search vs. binary search, benchmarked on synthetic data and on entity names
extracted with a Hugging Face NER model and stored in a Stardog knowledge graph.

University project for Advanced Programming / Data Structures and Algorithms.

## Table of contents

1. [Project status](#project-status)
2. [Requirements](#requirements)
3. [Getting the project](#getting-the-project)
4. [Setup](#setup)
5. [Running the code](#running-the-code)
6. [Running the tests](#running-the-tests)
7. [The algorithms](#the-algorithms)
8. [Project structure](#project-structure)
9. [Team workflow](#team-workflow)
10. [Troubleshooting](#troubleshooting)

## Project status

| Component | File | Status |
|---|---|---|
| Linear search (with `verbose`) | `linear_search.py` | Done |
| Binary search (with `verbose`) | `binary_search.py` | Done |
| Tests for both algorithms | `tests/` | Done (25 tests) |
| Benchmark data preparation | `prepare_data.py` | Done |
| Named Entity Recognition (Hugging Face) | `ner_extract.py` | Planned |
| Knowledge graph loading (Stardog) | `kg_loader.py` | Planned |
| Benchmark | `benchmark.py` | Planned |
| Plots | `plot_results.py` | Planned |
| Demo | `main.py` | Planned |

This table is updated whenever a component is merged.

## Requirements

- Python 3.12 or newer
- Git
- Around 5 GB of free disk space (`torch` and `transformers` are large packages)
- A Stardog Cloud account (only needed later, for the knowledge graph part)

## Getting the project

```
git clone https://github.com/shpres1mKrasniqi/search-algorithms-benchmark.git
cd search-algorithms-benchmark
```

To get the latest changes later:

```
git checkout main
git pull origin main
```

## Setup

Create a virtual environment and install the dependencies.

**Windows (PowerShell):**

```
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You should see `(.venv)` at the start of your terminal prompt when the environment
is active. In PyCharm, select the `.venv` interpreter under
Settings > Project > Python Interpreter.

Dependencies (`requirements.txt`):

| Package | Used for |
|---|---|
| `pytest` | Tests |
| `matplotlib` | Plots |
| `transformers`, `torch` | Named Entity Recognition (planned) |
| `datasets` | Loading a public dataset from the Hugging Face Hub (planned) |
| `pystardog` | Talking to Stardog (planned) |

## Running the code

Try linear search with step-by-step output:

```
python linear_search.py
```

Example output (shortened):

```
Searching for 5:
Step 1: items[0]=12 != target 5 -> next
...
Step 12: items[11]=5 == target 5 -> found
Result: (11, 12)
```

Both functions can also be used from your own code:

```python
from linear_search import linear_search
from binary_search import binary_search

print(linear_search([4, 8, 15, 16], 15))             # (2, 3)
print(binary_search([1, 3, 5, 7, 9, 11, 13], 7, verbose=True))
# Step 1: low=0 high=6 mid=3 items[3]=7 == target 7 -> found
# (3, 1)
```

A combined demo of both algorithms (`main.py`) will be added later.

## Running the tests

Run these from the project root with the virtual environment active:

```
pytest          # run all tests
pytest -v       # list every test with its result
pytest tests/test_linear_search.py     # one file only
```

Expected result: all tests pass (13 for linear search, 12 for binary search).
The settings are in `pytest.ini`, which makes the project root importable so
the tests can do `from linear_search import linear_search`.

What the tests cover:

- The target at the start, in the middle and at the end
- Targets that are not found
- Empty lists and lists with one element
- Duplicate elements
- Random inputs, checked against Python's built-in `in` / `list.index()`
- Comparison count boundaries (for example, exactly `n` comparisons when
  linear search does not find the target)
- Verbose mode printing the steps, and staying silent by default

## The algorithms

Both functions return a tuple `(index, comparisons)`. The index is `-1` when the
target is not found. One comparison is counted per loop iteration.

| | Linear search | Binary search |
|---|---|---|
| File | `linear_search.py` | `binary_search.py` |
| Input must be sorted | No | Yes |
| How it works | Checks elements from left to right | Repeatedly halves the search interval |
| Best case | O(1) | O(1) |
| Worst case | O(n) | O(log n) |
| Extra space | O(1) | O(1) |
| Duplicates | Returns the first match | Returns any matching index |

Both accept `verbose=True` to print every step. Verbose mode is off by default so
that printing does not distort the benchmark timings.

## Project structure

```
search-algorithms-benchmark/
├── linear_search.py     Linear search
├── binary_search.py     Binary search
├── prepare_data.py      Builds the sorted lists used by the benchmark
├── ner_extract.py       (planned) NER with Hugging Face
├── kg_loader.py         (planned) Stardog loading and SPARQL export
├── benchmark.py         (planned) Timing and comparison counts
├── plot_results.py      (planned) Plots from results/benchmark.csv
├── main.py              (planned) Demo for the presentation
├── tests/               pytest tests
├── data/                Input data (entities.csv, once exported from Stardog)
├── results/             Benchmark output (benchmark.csv and plots)
├── docs/                Report and slides
├── pytest.ini
├── requirements.txt
└── README.md
```

## Planned benchmark

Two scenarios, both searching for a target that does not exist (the worst case):

1. **Synthetic data:** `list(range(n))` for n = 1,000 / 5,000 / 10,000 / 50,000 /
   100,000 / 500,000 / 1,000,000.
2. **Knowledge graph data:** entity names from `data/entities.csv`, sorted
   alphabetically, in as many sizes as the extracted data allows.

Each measurement uses `time.perf_counter()`, is repeated five times, and the median
is stored. Comparison counts are recorded separately from time. Stardog query time
is not part of the benchmark. Results go to `results/benchmark.csv` with the
columns `dataset, algorithm, n, time_ms, comparisons`.

## Credentials

Stardog credentials must never be written in Python files or committed to Git.
They will be read from environment variables or a local `.env` file, which is
already listed in `.gitignore`. Exact variable names will be documented here when
`kg_loader.py` is added.

## Team workflow

- Each task is developed on its own branch named `task/<short-name>`
  (for example `task/linear-search`).
- Changes reach `main` through a pull request that the other team member reviews.
- Run `pytest` before opening a pull request.
- Tasks are tracked in Jira.

## Troubleshooting

**`ModuleNotFoundError: No module named 'linear_search'` when running pytest**
Run `pytest` from the project root (the folder that contains `pytest.ini`).

**PowerShell refuses to activate the virtual environment**
Run this once, then activate again:
```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**`pytest` or `pip` is not found**
The virtual environment is not active. Activate it (see Setup) and check that
`(.venv)` appears in your prompt.

**`pip install` takes very long**
`torch` is several hundred MB. This is normal on the first install.