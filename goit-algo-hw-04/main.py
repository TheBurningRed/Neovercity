
import time
from typing import Callable, Tuple, List


def measure_execution_time(func: Callable, arr: List[int]) -> Tuple[List[int], float]:
    """Measure the execution time of a sorting function.

    Args:
        func: The sorting function to measure
        arr: The array to sort

    Returns:
        A tuple containing the sorted array and execution time in milliseconds
    """
    start_time = time.perf_counter()
    result = func(arr)
    end_time = time.perf_counter()

    execution_time_ms = (end_time - start_time) * 1000
    return result, execution_time_ms


def insertion_sort(arr):
    a = arr[:] # clone
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    # recursive merge sort
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def timsort_builtin(arr):
    # Python sorted() = Timsort
    return sorted(arr)


def run_benchmarks(test_arrays: dict) -> None:
    """Run performance benchmarks for all sorting algorithms.

    Args:
        test_arrays: Dictionary with array names as keys and arrays as values
    """
    algorithms = {
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Timsort (Built-in)': timsort_builtin,
    }

    print("=" * 70)
    print("SORTING ALGORITHM PERFORMANCE METRICS")
    print("=" * 70)

    for array_name, arr in test_arrays.items():
        print(f"\nTest Array: {array_name} (Size: {len(arr)} elements)")
        print("-" * 70)
        print(f"{'Algorithm':<25} {'Execution Time (ms)':<20} {'Status':<20}")
        print("-" * 70)

        for algo_name, algo_func in algorithms.items():
            try:
                result, exec_time = measure_execution_time(algo_func, arr)

                # Verify the result is sorted
                is_sorted = result == sorted(arr)
                status = "✓ PASS" if is_sorted else "✗ FAIL"

                print(f"{algo_name:<25} {exec_time:<20.4f} {status:<20}")

            except Exception as e:
                print(f"{algo_name:<25} {'ERROR':<20} {str(e):<20}")

        print("-" * 70)


def main():
    """Main execution function with test cases."""
    # Create test arrays
    test_arrays = {
        'Small (10 elements)': [64, 34, 25, 12, 22, 11, 90, 88, 45, 50],
        'Medium (100 elements)': list(range(100, 0, -1)),  # Reverse sorted
        'Large (1000 elements)': [i * 7 % 1000 for i in range(1000)],  # Pseudo-random
    }

    # Run benchmarks
    run_benchmarks(test_arrays)

    print("\n" + "=" * 70)
    print("INDIVIDUAL EXECUTION EXAMPLES")
    print("=" * 70)

    # Example with small array
    test_arr = [5, 2, 8, 1, 9]
    print(f"\nOriginal array: {test_arr}")

    for algo_name, algo_func in [
        ('Insertion Sort', insertion_sort),
        ('Merge Sort', merge_sort),
        ('Timsort', timsort_builtin),
    ]:
        result, exec_time = measure_execution_time(algo_func, test_arr)
        print(f"{algo_name}: {result} (Time: {exec_time:.4f} ms)")


if __name__ == "__main__":
    main()
