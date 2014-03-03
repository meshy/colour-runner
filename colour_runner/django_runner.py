from .runner import ColouredTextTestRunner


class ColourRunnerMixin(object):
    test_runner = ColouredTextTestRunner

    def run_suite(self, suite, **kwargs):
        """This is the version from Django 1.7."""
        return self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)
