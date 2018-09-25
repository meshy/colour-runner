from unittest import runner

from .result import ColourTextTestResult


class ColourTextTestRunner(runner.TextTestRunner):
    """A test runner that uses colour in its output"""
    resultclass = ColourTextTestResult

    def __init__(self, *args, **kwargs):
        self.no_colour = kwargs.pop('no_colour', False)
        super(ColourTextTestRunner, self).__init__(*args, **kwargs)

    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity, self.no_colour)
