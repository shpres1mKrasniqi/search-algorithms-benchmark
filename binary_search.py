def binary_search(items, target, verbose=False):
    """Return (index, comparisons); index is -1 if not found.

    items must be sorted. One comparison = one loop iteration
    (one look at items[mid]).
    """
    low = 0
    high = len(items) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        if items[mid] == target:
            if verbose:
                print(f"Step {comparisons}: low={low} high={high} mid={mid} "
                      f"items[{mid}]={items[mid]!r} == target {target!r} -> found")
            return mid, comparisons

        if items[mid] < target:
            if verbose:
                print(f"Step {comparisons}: low={low} high={high} mid={mid} "
                      f"items[{mid}]={items[mid]!r} < target {target!r} -> go right")
            low = mid + 1
        else:
            if verbose:
                print(f"Step {comparisons}: low={low} high={high} mid={mid} "
                      f"items[{mid}]={items[mid]!r} > target {target!r} -> go left")
            high = mid - 1

    if verbose:
        print(f"Not found after {comparisons} comparisons")
    return -1, comparisons
