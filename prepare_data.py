"""Build the sorted lists that the benchmark searches in.

Two datasets:
  - synthetic: list(range(n)) for growing n
  - kg: entity names from data/entities.csv (exported from Stardog)

Both are returned sorted, so binary search can use them directly.
Linear search works on any order, so it uses the same lists.
"""

import csv
import random

SYNTHETIC_SIZES = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
KG_SIZES = [500, 1_000, 2_000, 5_000]
ENTITIES_CSV = "data/entities.csv"
SEED = 42


def synthetic_data(n):
    """Return the sorted list [0, 1, ..., n-1] and a target that is not in it."""
    items = list(range(n))
    target = n  # larger than every item -> worst case for both algorithms
    return items, target


def load_entities(path=ENTITIES_CSV):
    """Read the 'label' column of the csv and return the unique names, sorted."""
    # utf-8-sig also reads csv files saved by Excel/PowerShell (they add a BOM)
    with open(path, newline="", encoding="utf-8-sig") as f:
        names = {row["label"].strip() for row in csv.DictReader(f)}
    names.discard("")
    return sorted(names)


def kg_data(entities, n):
    """Pick n random entity names (fixed seed), sort them, add an absent target."""
    if n > len(entities):
        raise ValueError(f"asked for {n} entities, csv only has {len(entities)}")
    items = sorted(random.Random(SEED).sample(entities, n))
    target = items[-1] + "~"  # sorts after every name -> not in the list
    return items, target


if __name__ == "__main__":
    for n in SYNTHETIC_SIZES:
        items, target = synthetic_data(n)
        print(f"synthetic n={n:>9,}  first={items[0]}  last={items[-1]}  target={target}")

    try:
        entities = load_entities()
    except FileNotFoundError:
        print(f"\n{ENTITIES_CSV} not found yet, run kg_loader.py first.")
    else:
        print(f"\nloaded {len(entities)} unique entities")
        for n in KG_SIZES:
            if n <= len(entities):
                items, target = kg_data(entities, n)
                print(f"kg n={n:>5}  first={items[0]!r}  last={items[-1]!r}")
