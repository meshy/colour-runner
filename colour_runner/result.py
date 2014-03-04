from unittest import result
from unittest.util import strclass

from blessings import Terminal
from pygments import formatters, highlight
try:
    basestring  # Very crude check for python 3
    from pygments.lexers import Python3TracebackLexer as Lexer
except NameError:
    from pygments.lexers import PythonTracebackLexer as Lexer


class ColouredTextTestResult(result.TestResult):
    """
    A test result class that prints colour formatted text results to a stream.

    Based on https://github.com/python/cpython/blob/3.3/Lib/unittest/runner.py
    """
    formatter = formatters.Terminal256Formatter()
    lexer = Lexer()
    separator1 = '=' * 70
    separator2 = '-' * 70
    indent = '    '

    _terminal = Terminal()
    blue = _terminal.blue
    dim = _terminal.dim
    green = _terminal.green
    red = _terminal.bold_red
    yellow = _terminal.bold_yellow

    _test_class = None

    def __init__(self, stream, descriptions, verbosity):
        super(ColouredTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

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
            return doc.split('\n')[0].strip()
        return strclass(test_class)

    def startTest(self, test):
        super(ColouredTextTestResult, self).startTest(test)
        if self.showAll:
            if self._test_class != test.__class__:
                self._test_class = test.__class__
                self.stream.writeln(self.blue(self.getClassDescription(test)))
            self.stream.write(self.getShortDescription(test))
            self.stream.write(' ... ')
            self.stream.flush()

    def addSuccess(self, test):
        super(ColouredTextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln(self.green('ok'))
        elif self.dots:
            self.stream.write(self.green('.'))
            self.stream.flush()

    def addError(self, test, err):
        super(ColouredTextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln(self.red('ERROR'))
        elif self.dots:
            self.stream.write(self.red('E'))
            self.stream.flush()

    def addFailure(self, test, err):
        super(ColouredTextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln(self.yellow('FAIL'))
        elif self.dots:
            self.stream.write(self.yellow('F'))
            self.stream.flush()

    def addSkip(self, test, reason):
        super(ColouredTextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln('skipped {0!r}'.format(reason))
        elif self.dots:
            self.stream.write('s')
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(ColouredTextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln(self.green('expected failure'))
        elif self.dots:
            self.stream.write(self.green('x'))
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(ColouredTextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln(self.red('unexpected success'))
        elif self.dots:
            self.stream.write(self.red('u'))
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        colours = {'ERROR': self.red, 'FAIL': self.yellow}

        for test, err in errors:
            self.stream.writeln(self.separator1)
            title = "%s: %s" % (flavour, self.getLongDescription(test))
            self.stream.writeln(colours[flavour](title))
            self.stream.writeln(self.dim(self.separator2))
            self.stream.writeln(highlight(err, self.lexer, self.formatter))
