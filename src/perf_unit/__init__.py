"""
Copyright (c) 2022 Eldad Uzman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import time
import statistics
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

from contextlib import contextmanager
from unittest import TestCase


class NotATestCaseClass(Exception):
    """When the given class is not a subclass of unitetest.TestCase"""


@contextmanager
def time_block():
    """context manager for measuring the time it took to run a code block"""
    start_time = time.time()
    try:
        yield lambda: int((time.time() - start_time) * 1000)
    finally:
        pass


def run_single_iteration(
    method: callable, *args, delay_in_ms: int = 0, **kwargs
) -> int:
    """Running a single iteration of test method to allow distribution

    Args:
        method (callable): a method
        delay_in_ms (int, optional): the time it took to execute the method in milliseconds. Defaults to 0.

    Returns:
        int: _description_
    """
    with time_block() as duration:
        method(*args, **kwargs)
    time.sleep(delay_in_ms * 1000)
    return duration()


def perf_unit_test_class(
    *args,
    how_many_threads: int = 30,
    total_number_of_method_executions: int = 100,
    upper_median_threashold_in_milliseconds: int = 500,
    percentiles: tuple = (10, 50, 75, 90, 95, 99),
):
    """This class decorator converts all test methods in a unit test class into performance tests.

    It will run the method repeatedly, with a given number of concurrent threads and then analyzed the methods response time.


    Args:
        how_many_threads (int, optional): The number of concurrent threads to run the test method. Defaults to 30.
        total_number_of_method_executions (int, optional): Total number of runs for the method from all threads altogether. Defaults to 100.
        upper_median_threashold_in_milliseconds (int, optional): Threshold of the median response time to be asserted. Defaults to 500.
        percentiles (tuple, optional): Response time precentiles to be displyed at the end of the test execution. Defaults to (10, 50, 75, 90, 95, 99).
    """

    def modify_test_class(cls):
        def wrapper(method):
            @wraps(method)
            def wrapped_method(*args, **kwargs):
                futures = []
                with ThreadPoolExecutor(how_many_threads) as executor:
                    for _ in range(total_number_of_method_executions):
                        futures.append(
                            executor.submit(
                                run_single_iteration, method, *args, **kwargs
                            )
                        )

                execution_times = tuple([future.result() for future in futures])

                median_time = statistics.median(execution_times)

                print(
                    f"Percentile report for {method.__name__} with {len(execution_times)} calls:"
                )
                for p in percentiles:
                    print(
                        f"  {p}th percentile: {statistics.quantiles(execution_times, n=100)[p-1]} milliseconds"
                    )

                assert (
                    median_time < upper_median_threashold_in_milliseconds
                ), f"Median execution time is too high: {median_time} milliseconds"

            return wrapped_method

        if not issubclass(cls, TestCase):
            raise NotATestCaseClass(
                f"the given class `{cls.__name__}` is not a subclass of `unittest.TestCase`"
            )

        for attr in dir(cls):
            if attr.startswith("test_"):
                original_method = getattr(cls, attr)
                setattr(cls, attr, wrapper(original_method))

        return cls

    if len(args) == 1:
        return modify_test_class(args[0])

    return modify_test_class
