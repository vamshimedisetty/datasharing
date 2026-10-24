"""
Challenges 00: Python Basics
============================
Beginner coding challenges using only variables, math, if/else, loops and strings.
Replace each `pass` / TODO with your code, then run:  python3 00_basics_challenges.py
Each challenge prints PASS or FAIL. Do them in order; they get a little harder as you go.
"""


# --- Level 1: math & if/else ------------------------------------------------

def add(a, b):
    """Return the sum of a and b. (2, 3) -> 5"""
    pass  # TODO


def is_even(n):
    """Return True if n is even, otherwise False. 4 -> True, 7 -> False"""
    pass  # TODO


def max_of_three(a, b, c):
    """Return the largest of three numbers WITHOUT using max(). (3, 9, 5) -> 9"""
    pass  # TODO


def grade(score):
    """Return a letter grade: 90+ 'A', 80+ 'B', 70+ 'C', 60+ 'D', below 60 'F'."""
    pass  # TODO


def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit: F = C * 9 / 5 + 32. 100 -> 212.0"""
    pass  # TODO


def is_leap_year(year):
    """Leap year if divisible by 4, except centuries, unless divisible by 400.
    2024 -> True, 1900 -> False, 2000 -> True"""
    pass  # TODO


# --- Level 2: loops ---------------------------------------------------------

def sum_to_n(n):
    """Return 1 + 2 + ... + n using a loop. 5 -> 15"""
    pass  # TODO


def factorial(n):
    """Return n! = 1 * 2 * ... * n. 0! is 1. 5 -> 120"""
    pass  # TODO


def fizzbuzz(n):
    """Return a list for 1..n: 'Fizz' if divisible by 3, 'Buzz' by 5, 'FizzBuzz' by both,
    otherwise the number itself. 5 -> [1, 2, 'Fizz', 4, 'Buzz']"""
    pass  # TODO


def count_digits(n):
    """How many digits in a non-negative integer? 0 -> 1, 12345 -> 5"""
    pass  # TODO


def sum_of_digits(n):
    """Add up the digits of a non-negative integer. 1234 -> 10"""
    pass  # TODO


def is_prime(n):
    """Return True if n is prime (only divisible by 1 and itself). 7 -> True, 1 -> False"""
    pass  # TODO


def multiplication_table(n):
    """Return [n*1, n*2, ..., n*10]. 3 -> [3, 6, 9, ..., 30]"""
    pass  # TODO


# --- Level 3: strings -------------------------------------------------------

def reverse_string(s):
    """'hello' -> 'olleh'"""
    pass  # TODO


def is_palindrome(s):
    """Same forwards and backwards, ignoring case and spaces. 'Race car' -> True"""
    pass  # TODO


def count_vowels(s):
    """Count a, e, i, o, u (either case). 'Hello World' -> 3"""
    pass  # TODO


def capitalize_words(s):
    """Capitalize the first letter of every word. 'hello big world' -> 'Hello Big World'"""
    pass  # TODO


def most_common_char(s):
    """Return the character that appears most (ignore spaces). On a tie, the one seen first.
    'banana' -> 'a'"""
    pass  # TODO


def is_anagram(a, b):
    """Same letters in a different order, ignoring case. ('Listen', 'Silent') -> True"""
    pass  # TODO


def fibonacci(n):
    """Return the first n Fibonacci numbers. 7 -> [0, 1, 1, 2, 3, 5, 8]"""
    pass  # TODO


# ---------------------------------------------------------------------------
# Checks: no need to edit below this line.
# ---------------------------------------------------------------------------

def _check(name, func, cases):
    ok = True
    for args, expected in cases:
        try:
            got = func(*args)
        except Exception as e:  # noqa: BLE001
            got = f"{type(e).__name__}: {e}"
        if got != expected:
            ok = False
            print(f"  FAIL {name}{tuple(args)} -> expected {expected!r}, got {got!r}")
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    return ok


if __name__ == "__main__":
    results = [
        _check("add", add, [((2, 3), 5), ((-1, 1), 0)]),
        _check("is_even", is_even, [((4,), True), ((7,), False), ((0,), True)]),
        _check("max_of_three", max_of_three, [((3, 9, 5), 9), ((7, 2, 7), 7), ((-1, -5, -3), -1)]),
        _check("grade", grade, [((95,), "A"), ((80,), "B"), ((79,), "C"), ((60,), "D"), ((12,), "F")]),
        _check("celsius_to_fahrenheit", celsius_to_fahrenheit, [((100,), 212.0), ((0,), 32.0), ((-40,), -40.0)]),
        _check("is_leap_year", is_leap_year, [((2024,), True), ((1900,), False), ((2000,), True), ((2023,), False)]),
        _check("sum_to_n", sum_to_n, [((5,), 15), ((1,), 1), ((0,), 0)]),
        _check("factorial", factorial, [((5,), 120), ((0,), 1), ((1,), 1)]),
        _check("fizzbuzz", fizzbuzz, [((5,), [1, 2, "Fizz", 4, "Buzz"]),
                                      ((15,), [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
                                               11, "Fizz", 13, 14, "FizzBuzz"])]),
        _check("count_digits", count_digits, [((0,), 1), ((7,), 1), ((12345,), 5)]),
        _check("sum_of_digits", sum_of_digits, [((1234,), 10), ((0,), 0), ((99,), 18)]),
        _check("is_prime", is_prime, [((7,), True), ((1,), False), ((2,), True), ((9,), False), ((97,), True)]),
        _check("multiplication_table", multiplication_table, [((3,), [3, 6, 9, 12, 15, 18, 21, 24, 27, 30])]),
        _check("reverse_string", reverse_string, [(("hello",), "olleh"), (("",), "")]),
        _check("is_palindrome", is_palindrome, [(("Race car",), True), (("level",), True), (("python",), False)]),
        _check("count_vowels", count_vowels, [(("Hello World",), 3), (("AEIOU",), 5), (("xyz",), 0)]),
        _check("capitalize_words", capitalize_words, [(("hello big world",), "Hello Big World")]),
        _check("most_common_char", most_common_char, [(("banana",), "a"), (("abab",), "a"), (("a bb",), "b")]),
        _check("is_anagram", is_anagram, [(("Listen", "Silent"), True), (("abc", "abd"), False),
                                          (("aab", "abb"), False)]),
        _check("fibonacci", fibonacci, [((7,), [0, 1, 1, 2, 3, 5, 8]), ((1,), [0]), ((0,), [])]),
    ]
    print(f"\nScore: {sum(results)}/{len(results)}")
