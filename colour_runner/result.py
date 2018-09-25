from unittest import result
from unittest.util import strclass

from blessings import Terminal
from pygments import formatters, highlight
try:
    # Python 2
    text_type = unicode
    from pygments.lexers import PythonTracebackLexer as Lexer
except NameError:
    # Python 3
    text_type = str
    from pygments.lexers import Python3TracebackLexer as Lexer


class ColourTextTestResult(result.TestResult):
    """
    A test result class that prints colour formatted text results to a stream.

    Based on https://github.com/python/cpython/blob/3.3/Lib/unittest/runner.py
    """
    formatter = formatters.Terminal256Formatter()
    lexer = Lexer()
    separator1 = '=' * 70
    separator2 = '-' * 70
    indent = ' ' * 4

    _terminal = Terminal()
    colours = {
        None: text_type,
        'error': _terminal.bold_red,
        'expected': _terminal.blue,
        'fail': _terminal.bold_yellow,
        'skip': text_type,
        'success': _terminal.green,
        'title': _terminal.blue,
        'unexpected': _terminal.bold_red,
    }

    _test_class = None

    def __init__(self, stream, descriptions, verbosity, no_colour=False):
        super(ColourTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions
        self.no_colour = no_colour

    def getShortDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return self.indent + doc_first_line
        return self.indent + test._testMethodName

    def getLongDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        return str(test)

    def getClassDescription(self, test):
        test_class = test.__class__
        doc = test_class.__doc__
        if self.descriptions and doc:
            return doc.strip().split('\n')[0].strip()
        return strclass(test_class)

    def startTest(self, test):
        super(ColourTextTestResult, self).startTest(test)
        if self.showAll:
            if self._test_class != test.__class__:
                self._test_class = test.__class__
                title = self.getClassDescription(test)
                self.stream.writeln(self.colours['title'](title))
            self.stream.write(self.getShortDescription(test))
            self.stream.write(' ... ')
            self.stream.flush()

    def printResult(self, short, extended, colour_key=None):
        if self.no_colour:
            colour = self.colours[None]
        else:
            colour = self.colours[colour_key]
        if self.showAll:
            self.stream.writeln(colour(extended))
        elif self.dots:
            self.stream.write(colour(short))
            self.stream.flush()

    def addSuccess(self, test):
        super(ColourTextTestResult, self).addSuccess(test)
        self.printResult('.', 'ok', 'success')

    def addError(self, test, err):
        super(ColourTextTestResult, self).addError(test, err)
        self.printResult('E', 'ERROR', 'error')

    def addFailure(self, test, err):
        super(ColourTextTestResult, self).addFailure(test, err)
        self.printResult('F', 'FAIL', 'fail')

    def addSkip(self, test, reason):
        super(ColourTextTestResult, self).addSkip(test, reason)
        self.printResult('s', 'skipped {0!r}'.format(reason), 'skip')

    def addExpectedFailure(self, test, err):
        super(ColourTextTestResult, self).addExpectedFailure(test, err)
        self.printResult('x', 'expected failure', 'expected')

    def addUnexpectedSuccess(self, test):
        super(ColourTextTestResult, self).addUnexpectedSuccess(test)
        self.printResult('u', 'unexpected success', 'unexpected')

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        if self.no_colour:
            colour = self.colours[None]
        else:
            colour = self.colours[flavour.lower()]

        for test, err in errors:
            self.stream.writeln(self.separator1)
            title = '%s: %s' % (flavour, self.getLongDescription(test))
            self.stream.writeln(colour(title))
            self.stream.writeln(self.separator2)
            if self.no_colour:
                self.stream.writeln(err)
            else:
                self.stream.writeln(highlight(err, self.lexer, self.formatter))
