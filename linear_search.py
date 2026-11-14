def linear_search(items, target, verbose=False):
    comparisons = 0

    for index, value in enumerate(items):
        comparisons += 1

        if value == target:
            if verbose:
                print(f"Step {comparisons}: items[{index}]={value!r} "
                      f"== target {target!r} -> found")
            return index, comparisons

        if verbose:
            print(f"Step {comparisons}: items[{index}]={value!r} "
                  f"!= target {target!r} -> next")

    if verbose:
        print(f"Not found after {comparisons} comparisons")
    return -1, comparisons


if __name__ == "__main__":
    data = [12, 3, 43, 55, 67, 23, 5454, 675, 77, 88, 76, 5, 7, 874]
    print("Searching for 5:")
    print("Result:", linear_search(data, 5, verbose=True))
    print()
    print("Searching for 100:")
    print("Result:", linear_search(data, 100, verbose=True))