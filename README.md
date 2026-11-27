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
| Tests for both algorithms | `tests/` | Done (28 tests) |
| Benchmark data preparation | `prepare_data.py` | Done |
| Demo | `main.py` | Done |
| Named Entity Recognition (Hugging Face) | `ner_extract.py` | Done |
| Knowledge graph loading (Stardog) | `kg_loader.py` | Planned |
| Synthetic benchmark | `benchmark.py` | Done |
| Knowledge graph benchmark | `benchmark.py` | Planned |
| Plots | `plot_results.py` | Planned |

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
| `transformers`, `torch` | Named Entity Recognition |
| `datasets` | Loading the public AG News dataset |
| `pystardog` | Talking to Stardog (planned) |

## Running the code

Run commands from the project root, the folder containing `pytest.ini`.

### 1. Run the demo

The demo shows a found and a not-found target for both algorithms:

```
python main.py
```

It enables `verbose=True`, so each step is printed in the terminal.

### 2. Run the tests

```
pytest
```

The existing 28 tests cover the algorithms and NER helpers.

### 3. Test NER on three articles

On Windows PowerShell:

```powershell
$env:NUM_ARTICLES="3"
$env:CHUNK_SIZE="3"
$env:BATCH_SIZE="3"
python ner_extract.py
```

This loads three AG News articles, runs the Hugging Face NER model, removes
duplicates, and writes `data/entities.csv`.

The model and dataset require internet access the first time they are downloaded.

### 4. Run NER on the configured article count

Remove the PowerShell test variables if they are still set:

```powershell
Remove-Item Env:NUM_ARTICLES
Remove-Item Env:CHUNK_SIZE
Remove-Item Env:BATCH_SIZE
```

Then run:

```
python ner_extract.py
```

The default is 500 articles, unless `.env` overrides it.

### 5. Run the synthetic benchmark

```
python benchmark.py
```

This times both algorithms on the synthetic worst-case datasets and writes
`results/benchmark.csv`. Stardog is not needed for this run.

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
├── linear_search.py     Linear-search implementation
├── binary_search.py     Binary-search implementation
├── main.py              Algorithm demonstration
├── prepare_data.py      Builds synthetic and knowledge-graph lists
├── ner_extract.py       Loads AG News and extracts unique entities
├── kg_loader.py         Stardog loading and SPARQL export
├── benchmark.py         Timing and comparison measurements
├── plot_results.py      Future benchmark plots
├── tests/               Algorithm and NER tests
├── data/                Extracted entity input
├── results/             Benchmark CSV and generated plots
├── docs/
│   ├── report/          Written report
│   └── slides/          Presentation slides
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

## Stardog configuration

The knowledge graph part uses a Stardog Cloud database named `search-algorithms-benchmark`.
Credentials are never stored in the repository. They are read from a local `.env` file,
which is ignored by Git.

1. Copy the example file:
   ```
   copy .env.example .env        (Windows)
   cp .env.example .env          (macOS / Linux)
   ```
2. Fill in your own values in `.env`:
   ```
   STARDOG_ENDPOINT=https://<your-instance>.stardog.cloud:5820
   STARDOG_DATABASE=search-algorithms-benchmark
   STARDOG_USERNAME=<your Stardog user>
   STARDOG_PASSWORD=<your password>
   ```
3. Test the connection:
   ```
   python check_stardog_connection.py
   ```
   A result containing `'value': '0'` (an empty database) means it works.

Use a dedicated Stardog user with access to this database only. Never commit `.env`.

## Entity extraction (Hugging Face NER)

`ner_extract.py` reads news articles from the public `fancyzhx/ag_news` dataset and
extracts people (PER), organizations (ORG) and locations (LOC) with the pretrained model
`dslim/bert-base-NER`. No model is trained. The first run downloads the model
(about 400 MB) and the dataset into the local Hugging Face cache.

```
python ner_extract.py
```

Settings (model, dataset, number of articles, confidence threshold) have defaults in the
code and can be overridden in `.env`; see `.env.example`. Entities with a confidence
below 0.90, other types, or names that are very short or do not start with a letter or
digit are dropped. Example result: 2,000 articles give about 2,150 unique (name, type) pairs.