"""Time linear search vs. binary search and save the results to a csv.

Run 1: synthetic data, list(range(n)) for n = 1,000 ... 1,000,000
Run 2: knowledge graph data, entity names from data/entities.csv

Both runs use the worst case: the target is not in the list.
Only the search is timed. Building the lists and Stardog are not.
"""

import csv
import statistics
import time

from binary_search import binary_search
from linear_search import linear_search
from prepare_data import (KG_SIZES, SYNTHETIC_SIZES, kg_data, load_entities,
                          synthetic_data)

RESULTS_CSV = "results/benchmark.csv"
REPEATS = 5
ALGORITHMS = {"linear": linear_search, "binary": binary_search}


def loops_for(algorithm, n):
    """How many times to run one search inside a single timing.

    Binary search takes only microseconds, so one call is too short for the
    clock to measure reliably. We run it many times and divide.
    Linear search gets fewer loops as n grows, so every timing takes
    roughly the same wall time.
    """
    if algorithm == "binary":
        return 10_000
    return max(1, 1_000_000 // n)


def time_search(search, items, target, loops):
    """Return the median time of one search in milliseconds."""
    times = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        for _ in range(loops):
            search(items, target)
        end = time.perf_counter()
        times.append((end - start) / loops)
    return statistics.median(times) * 1000


def measure(dataset, n, items, target):
    """Run both algorithms on one list and return two result rows."""
    rows = []
    for name, search in ALGORITHMS.items():
        _, comparisons = search(items, target)
        time_ms = time_search(search, items, target, loops_for(name, n))
        rows.append({"dataset": dataset, "algorithm": name, "n": n,
                     "time_ms": time_ms, "comparisons": comparisons})
        print(f"{dataset:9} {name:6} n={n:>9,}  {time_ms:10.5f} ms  "
              f"{comparisons:>9,} comparisons")
    return rows


def run_synthetic():
    rows = []
    for n in SYNTHETIC_SIZES:
        items, target = synthetic_data(n)
        rows += measure("synthetic", n, items, target)
    return rows


def run_kg():
    try:
        entities = load_entities()
    except FileNotFoundError:
        print("data/entities.csv not found, skipping the knowledge graph run.")
        return []

    rows = []
    for n in KG_SIZES:
        if n > len(entities):
            print(f"only {len(entities)} entities, skipping n={n}")
            continue
        items, target = kg_data(entities, n)
        rows += measure("kg", n, items, target)
    return rows


def save(rows, path=RESULTS_CSV):
    fields = ["dataset", "algorithm", "n", "time_ms", "comparisons"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} rows to {path}")


if __name__ == "__main__":
    rows = run_synthetic() + run_kg()
    save(rows)
