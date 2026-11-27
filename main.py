from binary_search import binary_search
from linear_search import linear_search


def main():
    linear_items = [12, 3, 43, 55, 67, 23, 5454, 675, 77, 88, 76, 5, 7, 874]
    binary_items = [3, 5, 7, 12, 23, 43, 55, 67, 76, 77, 88, 675, 874, 5454]

    print("Linear search - found target")
    print("Result:", linear_search(linear_items, 43, verbose=True))

    print("\nLinear search - target not found")
    print("Result:", linear_search(linear_items, 100, verbose=True))

    print("\nBinary search - found target")
    print("Result:", binary_search(binary_items, 43, verbose=True))

    print("\nBinary search - target not found")
    print("Result:", binary_search(binary_items, 100, verbose=True))


if __name__ == "__main__":
    main()
