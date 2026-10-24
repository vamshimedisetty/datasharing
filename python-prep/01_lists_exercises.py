"""
Exercises 01: Python Lists
==========================
Replace each `pass` / TODO with your code, then run:  python3 01_lists_exercises.py
Each exercise prints PASS or FAIL. Keep going until everything passes.
Try to solve them without looking anything up first; check 01_lists_lesson.py if stuck.
"""


# --- Level 1: warm-up -------------------------------------------------------

def first_and_last(items):
    """Return a list with the first and last element. [1, 2, 3] -> [1, 3]"""
    pass  # TODO


def middle(items):
    """Return everything except the first and last. [1, 2, 3, 4] -> [2, 3]"""
    pass  # TODO


def reverse_list(items):
    """Return a NEW reversed list (do not change the input)."""
    pass  # TODO


def add_to_end(items, value):
    """Append value to items and return items. ([1, 2], 3) -> [1, 2, 3]"""
    pass  # TODO


# --- Level 2: core ----------------------------------------------------------

def total_and_average(numbers):
    """Return (total, average). Return (0, 0) for an empty list."""
    pass  # TODO


def count_greater_than(numbers, limit):
    """How many numbers are strictly greater than limit?"""
    pass  # TODO


def only_evens(numbers):
    """Return only the even numbers, keeping their order."""
    pass  # TODO


def remove_all(items, value):
    """Return a new list with every occurrence of value removed."""
    pass  # TODO


def second_largest(numbers):
    """Return the second largest DISTINCT number. [4, 9, 9, 2] -> 4. None if impossible."""
    pass  # TODO


# --- Level 3: interview-style -----------------------------------------------

def remove_duplicates(items):
    """Remove duplicates but keep the first-seen order. [3, 1, 3, 2, 1] -> [3, 1, 2]"""
    pass  # TODO


def rotate_left(items, k):
    """Rotate left by k. ([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]. Handle k > len and empty lists."""
    pass  # TODO


def merge_sorted(a, b):
    """Merge two already-sorted lists into one sorted list WITHOUT calling sort/sorted."""
    pass  # TODO


def chunk(items, size):
    """Split into chunks of `size`. ([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]"""
    pass  # TODO


def flatten(nested):
    """Flatten one level. [[1, 2], [3], []] -> [1, 2, 3]"""
    pass  # TODO


def two_sum(numbers, target):
    """Return indices [i, j] (i < j) of two numbers adding to target, or None. ([2, 7, 11, 15], 9) -> [0, 1]"""
    pass  # TODO


# ---------------------------------------------------------------------------
# Checks: no need to edit below this line.
# ---------------------------------------------------------------------------

def _check(name, func, cases):
    ok = True
    for args, expected in cases:
        try:
            got = func(*[a.copy() if isinstance(a, list) else a for a in args])
        except Exception as e:  # noqa: BLE001
            got = f"{type(e).__name__}: {e}"
        if got != expected:
            ok = False
            print(f"  FAIL {name}{tuple(args)} -> expected {expected!r}, got {got!r}")
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    return ok


def _no_mutation():
    data = [1, 2, 3]
    reverse_list(data)
    return data == [1, 2, 3]


if __name__ == "__main__":
    results = [
        _check("first_and_last", first_and_last, [(([1, 2, 3],), [1, 3]), ((["a"],), ["a", "a"])]),
        _check("middle", middle, [(([1, 2, 3, 4],), [2, 3]), (([1, 2],), [])]),
        _check("reverse_list", reverse_list, [(([1, 2, 3],), [3, 2, 1]), (([],), [])]),
        _check("reverse_list keeps input", lambda: _no_mutation(), [((), True)]),
        _check("add_to_end", add_to_end, [(([1, 2], 3), [1, 2, 3]), (([], "x"), ["x"])]),
        _check("total_and_average", total_and_average, [(([2, 4, 6],), (12, 4.0)), (([],), (0, 0))]),
        _check("count_greater_than", count_greater_than, [(([1, 5, 8, 3, 9], 4), 3), (([], 0), 0)]),
        _check("only_evens", only_evens, [(([1, 2, 3, 4, 6],), [2, 4, 6]), (([1, 3],), [])]),
        _check("remove_all", remove_all, [(([1, 2, 1, 3, 1], 1), [2, 3]), ((["a"], "b"), ["a"])]),
        _check("second_largest", second_largest, [(([4, 9, 9, 2],), 4), (([5, 5],), None), (([],), None)]),
        _check("remove_duplicates", remove_duplicates, [(([3, 1, 3, 2, 1],), [3, 1, 2]), (([],), [])]),
        _check("rotate_left", rotate_left, [(([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2]),
                                            (([1, 2, 3], 4), [2, 3, 1]), (([], 3), [])]),
        _check("merge_sorted", merge_sorted, [(([1, 4, 7], [2, 3, 8, 9]), [1, 2, 3, 4, 7, 8, 9]),
                                              (([], [1]), [1])]),
        _check("chunk", chunk, [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]), (([], 3), [])]),
        _check("flatten", flatten, [(([[1, 2], [3], []],), [1, 2, 3])]),
        _check("two_sum", two_sum, [(([2, 7, 11, 15], 9), [0, 1]), (([3, 2, 4], 6), [1, 2]),
                                    (([1, 2], 10), None)]),
    ]
    print(f"\nScore: {sum(results)}/{len(results)}")
