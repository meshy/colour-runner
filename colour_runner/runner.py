from unittest import runner

from .result import ColouredTextTestResult


class ColouredTextTestRunner(runner.TextTestRunner):
    """A test runner that uses colour in its output"""
    resultclass = ColouredTextTestResult
