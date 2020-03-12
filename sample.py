"""Simple application of the BusyBee module for an intentionally slow prime
number check. The expected linear execution time is ~50 seconds. On an 8
core machine we'd expect around ~6-7 seconds run time.
"""

import busybee
import math
import random
import time


def slow_prime_check(number):
    """This function is an intentionally slow and simple prime number check."""

    # average wait time ~50ms.
    time.sleep(100 / 1000 * random.random())

    for i in range(2, int(math.sqrt(number)+1)):
        if number % i == 0:
            return False
    return True


if __name__ == "__main__":
    a, b = 1_000, 2_000
    numbers = range(a, b)
    is_prime = busybee.map(slow_prime_check, numbers, update_every_n_seconds=2)

    print()
    print("Found %d prime numbers between %d and %d" % (sum(is_prime), a, b))
