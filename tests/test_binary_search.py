import math
import random

from binary_search import binary_search

ITEMS = [1, 3, 5, 7, 9, 11, 13]


def test_found_at_start():
    assert binary_search(ITEMS, 1)[0] == 0


def test_found_in_middle():
    assert binary_search(ITEMS, 7)[0] == 3


def test_found_at_end():
    assert binary_search(ITEMS, 13)[0] == 6


def test_smaller_than_all():
    assert binary_search(ITEMS, 0)[0] == -1


def test_larger_than_all():
    assert binary_search(ITEMS, 14)[0] == -1


def test_between_items():
    assert binary_search(ITEMS, 6)[0] == -1


def test_empty_list():
    assert binary_search([], 5) == (-1, 0)


def test_single_element():
    assert binary_search([5], 5) == (0, 1)
    assert binary_search([5], 4) == (-1, 1)


def test_duplicates():
    items = [1, 2, 2, 2, 3]
    idx, _ = binary_search(items, 2)
    assert items[idx] == 2  # any of the 2s is a correct answer


def test_strings():
    names = ["Berlin", "Google", "Paris", "Zurich"]
    assert binary_search(names, "Paris")[0] == 2
    assert binary_search(names, "London")[0] == -1


def test_matches_python_in():
    rng = random.Random(0)
    for _ in range(200):
        items = sorted(rng.sample(range(1000), rng.randint(0, 50)))
        target = rng.randint(-10, 1010)
        idx, _ = binary_search(items, target)
        assert (idx != -1) == (target in items)
        if idx != -1:
            assert items[idx] == target


def test_worst_case_comparisons():
    for n in [1, 2, 3, 10, 100, 1000, 1_000_000]:
        items = list(range(n))
        _, comps = binary_search(items, n)  # absent, larger than all
        assert comps <= math.floor(math.log2(n)) + 1
