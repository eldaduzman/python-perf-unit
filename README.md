# python-perf-unit


[![Version](https://img.shields.io/pypi/v/python-perf-unit)](https://pypi.python.org/pypi/python-perf-unit)
![](https://raw.githubusercontent.com/eldaduzman/python-perf-unit/main/docs/badges/coverage-badge.svg)
![](https://raw.githubusercontent.com/eldaduzman/python-perf-unit/main/docs/badges/pylint.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`python-perf-unit` is a Python package designed to enhance unit testing with performance metrics. By integrating with Python's unittest framework, it enables the execution of test methods with performance analysis.

## Features

- **Performance Testing**: Automatically times unittest test methods.
- **Median Execution Time Assertion**: Asserts median execution time of test methods is below a specified threshold.
- **Parallel Execution**: Runs tests in parallel using multithreading.
- **Percentile Reporting**: Detailed percentile reports for test execution times.

## Installation

```bash
pip install python-perf-unit
```

## Usage
Decorate your unittest class with `@perf_unit_test_class` to turn standard unit tests into performance tests.

```python

from perf_unit import perf_unit_test_class
import unittest

@perf_unit_test_class
class MyTestCase(unittest.TestCase):

    def test_example1(self):
        # Your test code here
        pass

    def test_example2(self):
        # Another test code
        pass

if __name__ == '__main__':
    unittest.main()


```

## Code styling
### `black` used for auto-formatting code [read](https://pypi.org/project/black/),
### `pylint` used for code linting and pep8 compliance [read](https://pypi.org/project/pylint/),
### `mypy` used for type hinting [read](https://pypi.org/project/mypy/),