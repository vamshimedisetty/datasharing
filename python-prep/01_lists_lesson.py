"""
Lesson 01: Python Lists
=======================
A list is an ordered, changeable collection that can hold any type of value.
Run this file and read the output next to the code:  python3 01_lists_lesson.py
"""


def section(title):
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------------------
section("1. Creating lists")
empty = []
numbers = [10, 20, 30, 40, 50]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "two", 3.0, True, None]      # any types are allowed
nested = [[1, 2], [3, 4]]                # lists inside lists
from_range = list(range(5))              # [0, 1, 2, 3, 4]
from_string = list("abc")                # ['a', 'b', 'c']
print(empty, numbers, fruits, mixed, nested, from_range, from_string, sep="\n")
print("length of numbers:", len(numbers))

# ---------------------------------------------------------------------------
section("2. Indexing (positions start at 0)")
#            index:  0   1   2   3   4
#   negative index: -5  -4  -3  -2  -1
print("numbers[0]  =", numbers[0])       # first
print("numbers[2]  =", numbers[2])
print("numbers[-1] =", numbers[-1])      # last
print("numbers[-2] =", numbers[-2])      # second to last
print("nested[1][0] =", nested[1][0])    # row 1, column 0 -> 3
# numbers[10] would raise IndexError

# ---------------------------------------------------------------------------
section("3. Slicing  list[start:stop:step]  (stop is NOT included)")
print("numbers[1:4]  =", numbers[1:4])   # [20, 30, 40]
print("numbers[:3]   =", numbers[:3])    # first 3
print("numbers[2:]   =", numbers[2:])    # from index 2 to end
print("numbers[::2]  =", numbers[::2])   # every 2nd item
print("numbers[::-1] =", numbers[::-1])  # reversed copy
print("numbers[:]    =", numbers[:])     # shallow copy

# ---------------------------------------------------------------------------
section("4. Changing items")
colors = ["red", "green", "blue"]
colors[1] = "yellow"
print("after colors[1] = 'yellow':", colors)
colors[0:2] = ["black", "white"]
print("after slice assignment:   ", colors)

# ---------------------------------------------------------------------------
section("5. Adding items")
nums = [1, 2, 3]
nums.append(4)              # add ONE item at the end
print("append(4):        ", nums)
nums.insert(0, 0)           # insert at a position
print("insert(0, 0):     ", nums)
nums.extend([5, 6])         # add MANY items at the end
print("extend([5, 6]):   ", nums)
combined = nums + [7, 8]    # + makes a NEW list
print("nums + [7, 8]:    ", combined)
print("[0] * 3:          ", [0] * 3)

# Common trap: append vs extend
a = [1, 2]; a.append([3, 4]); print("append([3,4]) ->", a)   # [1, 2, [3, 4]]
b = [1, 2]; b.extend([3, 4]); print("extend([3,4]) ->", b)   # [1, 2, 3, 4]

# ---------------------------------------------------------------------------
section("6. Removing items")
pets = ["cat", "dog", "fish", "dog", "bird"]
pets.remove("dog")          # removes FIRST matching value
print("remove('dog'):", pets)
last = pets.pop()           # removes & returns last item
print("pop() returned", repr(last), "->", pets)
first = pets.pop(0)         # removes & returns item at index
print("pop(0) returned", repr(first), "->", pets)
del pets[0]                 # delete by index (no return value)
print("del pets[0]:  ", pets)
pets.clear()
print("clear():      ", pets)

# ---------------------------------------------------------------------------
section("7. Searching & counting")
letters = ["a", "b", "c", "b", "a", "b"]
print("'b' in letters    :", "b" in letters)
print("'z' not in letters:", "z" not in letters)
print("letters.count('b'):", letters.count("b"))
print("letters.index('c'):", letters.index("c"))   # ValueError if missing

# ---------------------------------------------------------------------------
section("8. Sorting & ordering")
scores = [88, 42, 95, 67, 73]
print("sorted(scores)              :", sorted(scores))          # new list
print("sorted(scores, reverse=True):", sorted(scores, reverse=True))
print("scores unchanged            :", scores)
scores.sort()                                                   # in place, returns None
print("after scores.sort()         :", scores)
scores.reverse()
print("after scores.reverse()      :", scores)
words = ["banana", "Apple", "kiwi", "cherry"]
print("sort by length:", sorted(words, key=len))
print("case-insensitive:", sorted(words, key=str.lower))

# ---------------------------------------------------------------------------
section("9. Useful built-ins")
data = [4, 8, 15, 16, 23, 42]
print("len:", len(data), "| sum:", sum(data), "| min:", min(data), "| max:", max(data))
print("average:", sum(data) / len(data))

# ---------------------------------------------------------------------------
section("10. Looping")
for fruit in fruits:
    print("fruit:", fruit)
for i, fruit in enumerate(fruits):          # index + value
    print(f"{i}: {fruit}")
prices = [1.2, 0.5, 3.0]
for fruit, price in zip(fruits, prices):    # walk two lists together
    print(f"{fruit} costs ${price}")

# ---------------------------------------------------------------------------
section("11. List comprehensions (build a list in one line)")
squares = [n * n for n in range(1, 6)]
evens = [n for n in range(10) if n % 2 == 0]
upper = [f.upper() for f in fruits]
print("squares:", squares)
print("evens:  ", evens)
print("upper:  ", upper)
# Same as squares, written as a loop:
squares_loop = []
for n in range(1, 6):
    squares_loop.append(n * n)
print("loop version equal?", squares == squares_loop)

# ---------------------------------------------------------------------------
section("12. Copying: the #1 beginner trap")
original = [1, 2, 3]
alias = original            # NOT a copy, both names point to the same list
alias.append(99)
print("original after alias.append(99):", original)   # changed too!
original = [1, 2, 3]
copy1 = original.copy()     # or original[:] or list(original)
copy1.append(99)
print("original after copy1.append(99):", original)   # unchanged

# Another trap: building a grid with *
bad_grid = [[0] * 3] * 2    # both rows are the SAME list
bad_grid[0][0] = 1
print("bad grid: ", bad_grid)
good_grid = [[0] * 3 for _ in range(2)]
good_grid[0][0] = 1
print("good grid:", good_grid)

# ---------------------------------------------------------------------------
section("13. Unpacking")
point = [3, 7]
x, y = point
print("x =", x, "y =", y)
head, *rest = [1, 2, 3, 4]
print("head =", head, "rest =", rest)

print("\nDone! Now open 01_lists_exercises.py and try the practice problems.")
