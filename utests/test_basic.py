"""unittest module"""
import random
import time
from unittest import TestCase, main, TestLoader, TextTestRunner

from perf_unit import NotATestCaseClass, perf_unit_test_class


class TestBasic(TestCase):
    def test_basic_test_class(self):
        @perf_unit_test_class(how_many_threads=50)
        class SomeTestClass(TestCase):
            def test_method(false_self):
                time.sleep(random.randint(200, 600) / 1000)

        suite = TestLoader().loadTestsFromTestCase(SomeTestClass)

        runner = TextTestRunner()
        result = runner.run(suite)
        result.printErrors()
        self.assertTrue(result.wasSuccessful())

    def test_should_fail_due_too_high_latency(self):
        @perf_unit_test_class(how_many_threads=50, upper_median_threashold_in_milliseconds=1)
        class SomeTestClass(TestCase):
            def test_method(false_self):
                time.sleep(random.randint(200, 600) / 1000)

        suite = TestLoader().loadTestsFromTestCase(SomeTestClass)

        runner = TextTestRunner()
        result = runner.run(suite)
        result.printErrors()
        self.assertFalse(result.wasSuccessful())

    def test_class_is_not_unit_test_subclass(self):
        with self.assertRaises(NotATestCaseClass) as exp:

            @perf_unit_test_class(how_many_threads=50)
            class SomeTestClass:
                pass

        self.assertEqual(
            str(exp.exception),
            "the given class `SomeTestClass` is not a subclass of `unittest.TestCase`",
        )

    def test_class_has_no_test_methods(self):
        @perf_unit_test_class(how_many_threads=50)
        class SomeTestClass(TestCase):
            pass


if __name__ == "__main__":
    main()
