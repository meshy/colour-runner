from unittest import runner

from .result import ColourTextTestResult


class ColourTextTestRunner(runner.TextTestRunner):
    """A test runner that uses colour in its output"""
    resultclass = ColourTextTestResult
