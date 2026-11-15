import random

from linear_search import linear_search

ITEMS = [4, 8, 15, 16, 23, 42]


def test_found_at_start():
    assert linear_search(ITEMS, 4) == (0, 1)


def test_found_in_middle():
    assert linear_search(ITEMS, 15) == (2, 3)


def test_found_at_end():
    assert linear_search(ITEMS, 42) == (5, 6)


def test_not_found():
    assert linear_search(ITEMS, 99) == (-1, 6)


def test_empty_list():
    assert linear_search([], 5) == (-1, 0)


def test_single_element():
    assert linear_search([5], 5) == (0, 1)
    assert linear_search([5], 4) == (-1, 1)


def test_duplicates_returns_first_match():
    assert linear_search([7, 3, 7, 7], 7) == (0, 1)
    assert linear_search([1, 2, 2, 2], 2) == (1, 2)


def test_unsorted_input():
    assert linear_search([9, 1, 5, 3], 5) == (2, 3)


def test_strings():
    names = ["Paris", "Google", "Zurich", "Berlin"]
    assert linear_search(names, "Zurich") == (2, 3)
    assert linear_search(names, "London") == (-1, 4)


def test_matches_python_index():
    rng = random.Random(0)
    for _ in range(200):
        items = [rng.randint(0, 100) for _ in range(rng.randint(0, 50))]
        target = rng.randint(-10, 110)
        idx, comps = linear_search(items, target)
        if target in items:
            assert idx == items.index(target)
            assert comps == idx + 1
        else:
            assert idx == -1
            assert comps == len(items)


def test_comparison_count_boundaries():
    for n in [1, 2, 10, 1000, 100_000]:
        items = list(range(n))
        assert linear_search(items, 0)[1] == 1
        assert linear_search(items, n - 1)[1] == n
        assert linear_search(items, n)[1] == n


def test_verbose_prints_steps(capsys):
    linear_search([4, 8, 15], 8, verbose=True)
    output = capsys.readouterr().out
    assert "Step 1" in output
    assert "Step 2" in output
    assert "found" in output
    assert "Step 3" not in output


def test_verbose_off_prints_nothing(capsys):
    linear_search([4, 8, 15], 99)
    assert capsys.readouterr().out == ""